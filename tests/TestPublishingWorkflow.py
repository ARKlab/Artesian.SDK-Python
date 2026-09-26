import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/python-tests.yml"


class TestPublishingWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(WORKFLOW.read_text())

    def test_supported_python_versions_get_linted_and_tested(self):
        jobs = self.workflow["jobs"]
        versions = jobs["build"]["strategy"]["matrix"]["python-version"]
        self.assertEqual(versions, ["3.11", "3.12", "3.13", "3.14"])
        self.assertEqual(jobs["quality"]["steps"][1]["with"]["python-version"], "3.14")
        build = jobs["build"]
        self.assertEqual(build["strategy"]["matrix"]["os"], ["ubuntu-latest", "windows-latest", "macos-latest"])
        self.assertEqual(build["steps"][1]["with"]["python-version"], "${{ matrix.python-version }}")
        steps = {step["name"]: step for step in build["steps"]}
        self.assertIn("uv sync --locked", steps["Install dependencies"]["run"])
        lint = steps["Run Ruff and Pyrefly"]["run"]
        for command in ("ruff check", "ruff format --check", "pyrefly check"):
            self.assertIn(command, lint)
        self.assertIn("--target-version", lint)
        self.assertIn("--python-version \"$PYTHON_VERSION\"", lint)
        self.assertEqual(steps["Run Ruff and Pyrefly"]["env"]["PYTHON_VERSION"], "${{ matrix.python-version }}")
        self.assertIn("pytest", steps["Test Pytest"]["run"])

    def test_release_builds_are_separate_from_publisher(self):
        jobs = self.workflow["jobs"]
        publish = jobs["publish"]
        producers = ("build-stable", "build-beta", "build-preview")
        self.assertEqual(set(publish["needs"]), set(producers))
        self.assertIn("!failure()", publish["if"])
        for name in producers:
            self.assertIn(f"needs.{name}.result == 'success'", publish["if"])
            build = jobs[name]
            self.assertNotEqual(build.get("permissions", {}).get("id-token"), "write")
            steps = {step["name"]: step for step in build["steps"]}
            self.assertIn("quality", build["needs"])
            self.assertIn("build", build["needs"])
            self.assertIn("validate_tag.sh", next(s["run"] for s in build["steps"] if "Validate" in s["name"] and "tag" in s["name"]))
            self.assertIn("twine check dist/*", steps["Check release metadata"]["run"])
            self.assertIn("git rev-parse HEAD", steps["Record release source"]["run"])
            self.assertIn("sha256sum dist/*.whl dist/*.tar.gz", steps["Record distribution hashes"]["run"])
            self.assertEqual(steps["Upload release distributions"]["with"]["name"], "release-dist")
        preview = jobs["build-preview"]["steps"]
        self.assertEqual(next(s["with"]["ref"] for s in preview if s["name"] == "Checkout merged PR head"),
                         "refs/pull/${{ steps.pr.outputs.number }}/merge")

    def test_publisher_uses_uv_attestations_without_running_build_code(self):
        jobs = self.workflow["jobs"]
        self.assertEqual([name for name, job in jobs.items() if job.get("permissions", {}).get("id-token") == "write"],
                         ["publish"])
        publish = jobs["publish"]
        self.assertEqual(publish["environment"]["name"], "pypi")
        self.assertEqual([s["name"] for s in publish["steps"]], [
            "Download release distributions", "Check release filenames", "Set up pinned uv",
            "Generate PEP 740 publish attestations", "Publish with required Trusted Publishing",
        ])
        download, _, setup, attest, upload = publish["steps"]
        self.assertEqual(download["with"], {"name": "release-dist", "path": "dist"})
        self.assertEqual(setup["with"]["version"], "0.12.19")
        self.assertRegex(attest["uses"], r"^astral-sh/attest-action@[0-9a-f]{40}$")
        self.assertIn("dist/*.whl", attest["with"]["paths"])
        self.assertIn("dist/*.tar.gz", attest["with"]["paths"])
        self.assertIn("uv publish --no-config --trusted-publishing always", upload["run"])
        self.assertIn("https://upload.pypi.org/legacy/", upload["run"])
        self.assertFalse(any("actions/checkout" in s.get("uses", "") for s in publish["steps"]))

    def test_publisher_rejects_distributions_outside_release_tag(self):
        step = next(s for s in self.workflow["jobs"]["publish"]["steps"] if s["name"] == "Check release filenames")
        self.assertEqual(step["shell"], "python")
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                dist = Path("dist")
                dist.mkdir()
                for tag, version in (
                    ("v4.3.0", "4.3.0"),
                    ("v4.3.0b2", "4.3.0b2"),
                    ("v04.03.00a069.02", "4.3.0a69.post2"),
                ):
                    with self.subTest(tag=tag), patch.dict(os.environ, {"GITHUB_REF_NAME": tag}):
                        for path in dist.iterdir():
                            path.unlink()
                        (dist / f"artesian_sdk-{version}-py3-none-any.whl").touch()
                        (dist / f"artesian_sdk-{version}.tar.gz").touch()
                        exec(compile(step["run"], str(WORKFLOW), "exec"), {})
                        (dist / "other.whl").touch()
                        with self.assertRaisesRegex(SystemExit, "do not match"):
                            exec(compile(step["run"], str(WORKFLOW), "exec"), {})
                        (dist / "other.whl").unlink()
                        with patch.dict(os.environ, {"GITHUB_REF_NAME": "v9.9.9"}):
                            with self.assertRaisesRegex(SystemExit, "do not match"):
                                exec(compile(step["run"], str(WORKFLOW), "exec"), {})
            finally:
                os.chdir(previous)
