import os
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/python-tests.yml"


class TestPublishingWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = yaml.safe_load(WORKFLOW.read_text())

    def test_supported_python_versions_get_linted_and_tested(self) -> None:
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
        self.assertIn('--python-version "$PYTHON_VERSION"', lint)
        self.assertEqual(steps["Run Ruff and Pyrefly"]["env"]["PYTHON_VERSION"], "${{ matrix.python-version }}")
        self.assertIn("pytest", steps["Test Pytest"]["run"])

    def test_test_sources_are_included_in_lint_and_typing(self) -> None:
        config = tomllib.loads((WORKFLOW.parents[2] / "pyproject.toml").read_text())
        self.assertNotIn("tests", config["tool"]["ruff"]["extend-exclude"])
        self.assertIn("tests", config["tool"]["pyrefly"]["project-includes"])

    def test_release_builds_are_separate_from_publisher(self) -> None:
        jobs = self.workflow["jobs"]
        publish = jobs["publish"]
        producers = ("build-stable", "build-beta", "build-preview")
        self.assertEqual(set(publish["needs"]), {*producers, "test-report", "coverage-report"})
        self.assertIn("!failure()", publish["if"])
        for name in ("test-report", "coverage-report"):
            self.assertIn(f"needs.{name}.result == 'success'", publish["if"])
        for name in producers:
            self.assertIn(f"needs.{name}.result == 'success'", publish["if"])
            build = jobs[name]
            self.assertNotEqual(build.get("permissions", {}).get("id-token"), "write")
            steps = {step["name"]: step for step in build["steps"]}
            self.assertIn("quality", build["needs"])
            self.assertIn("build", build["needs"])
            self.assertIn(
                "validate_tag.sh",
                next(s["run"] for s in build["steps"] if "Validate" in s["name"] and "tag" in s["name"]),
            )
            self.assertIn("twine check dist/*", steps["Check release metadata"]["run"])
            self.assertIn("git rev-parse HEAD", steps["Record release source"]["run"])
            self.assertIn("sha256sum dist/*.whl dist/*.tar.gz", steps["Record distribution hashes"]["run"])
            self.assertEqual(steps["Upload release distributions"]["with"]["name"], "release-dist")
            self.assertEqual(
                next(s["with"]["ref"] for s in build["steps"] if s.get("uses", "").startswith("actions/checkout@")),
                "${{ github.sha }}",
            )
        preview = jobs["build-preview"]["steps"]
        ancestry = next(s["run"] for s in preview if s["name"] == "Validate preview source")
        self.assertIn("git merge-base --is-ancestor origin/master HEAD", ancestry)
        self.assertIn('git fetch origin "refs/pull/$PR_NUMBER/head"', ancestry)
        self.assertIn("git rev-parse FETCH_HEAD^{commit}", ancestry)
        self.assertIn("git merge-base --is-ancestor HEAD origin/master", ancestry)

    def test_release_events_require_a_tag_and_validation(self) -> None:
        jobs = self.workflow["jobs"]
        triggers = self.workflow.get("on", self.workflow.get(True))
        self.assertIn("pull_request", triggers)
        self.assertIn("workflow_dispatch", triggers)
        self.assertIn("tags", triggers["push"])
        self.assertNotIn("ref", jobs["quality"]["steps"][0]["with"])
        for name in ("build-stable", "build-beta", "build-preview", "publish"):
            condition = jobs[name]["if"]
            self.assertIn("(github.event_name == 'push' || github.event_name == 'workflow_dispatch')", condition)
            self.assertIn("startsWith(github.ref, 'refs/tags/v')", condition)
        for name in ("build-stable", "build-beta", "build-preview"):
            self.assertIn("quality", jobs[name]["needs"])
            self.assertIn("build", jobs[name]["needs"])
        self.assertEqual(jobs["coverage-report"]["needs"], ["build"])

    def test_preview_source_must_belong_to_the_tagged_pr(self) -> None:
        steps = self.workflow["jobs"]["build-preview"]["steps"]
        script = next(s["run"] for s in steps if s["name"] == "Validate preview source")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work = root / "work"
            work.mkdir()
            subprocess.run(["git", "init", "--bare", str(root / "origin.git")], check=True, capture_output=True)

            def git(*args: str) -> None:
                subprocess.run(["git", *args], cwd=work, check=True, capture_output=True)

            git("init", "-b", "master")
            git("config", "user.name", "CI")
            git("config", "user.email", "ci@example.invalid")
            git("remote", "add", "origin", str(root / "origin.git"))
            git("commit", "--allow-empty", "-m", "base")
            git("push", "origin", "master")
            git("checkout", "-b", "feature")
            git("commit", "--allow-empty", "-m", "feature")
            feature_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=work, text=True).strip()
            git("push", "origin", "HEAD:refs/pull/69/head")
            git("push", "origin", "master:refs/pull/70/head")
            git("commit", "--allow-empty", "-m", "stacked feature")
            git("push", "origin", "HEAD:refs/pull/71/head")
            git("checkout", "--detach", "HEAD^")
            for ref, tag, valid in (
                ("HEAD", "v4.3.0a69.1", True),
                ("HEAD", "v4.3.0a70.1", False),
                ("HEAD", "v4.3.0a71.1", False),
                ("master", "v4.3.0a69.1", False),
            ):
                with self.subTest(ref=ref, tag=tag):
                    git("checkout", "--detach", ref)
                    result = subprocess.run(
                        ["bash", "-e", "-o", "pipefail", "-c", script],
                        cwd=work,
                        env={**os.environ, "GITHUB_REF_NAME": tag},
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(result.returncode == 0, valid, result.stderr)

            git("checkout", "--detach", feature_sha)
            git("tag", "v4.3.0a69.1")
            git("push", "origin", "v4.3.0a69.1")
            validator = str(WORKFLOW.parent / "validate_tag.sh")
            env = {**os.environ, "GITHUB_REF": "refs/tags/v4.3.0a69.1"}
            command = ["bash", validator, "v4.3.0a69.1", "preview"]
            valid_tag = subprocess.run(command, cwd=work, env=env, capture_output=True, check=False)
            self.assertEqual(valid_tag.returncode, 0, valid_tag.stderr)
            git("tag", "-f", "v4.3.0a69.1", "master")
            git("push", "--force", "origin", "v4.3.0a69.1")
            moved_tag = subprocess.run(command, cwd=work, env=env, capture_output=True, check=False)
            self.assertNotEqual(moved_tag.returncode, 0, moved_tag.stderr)
            git("tag", "-fa", "v4.3.0a69.1", "-m", "annotated release", "master")
            branch_validator = str(WORKFLOW.parent / "validate_branch.sh")
            env["GITHUB_SHA"] = subprocess.check_output(
                ["git", "rev-parse", "refs/tags/v4.3.0a69.1"], cwd=work, text=True
            ).strip()
            branch_check = subprocess.run(
                ["bash", branch_validator, "master"], cwd=work, env=env, capture_output=True, check=False
            )
            self.assertEqual(branch_check.returncode, 0, branch_check.stderr)
            git("tag", "-f", "v4.3.0a69.1", feature_sha)
            git("checkout", "--detach", "master")
            branch_check = subprocess.run(
                ["bash", branch_validator, "master"], cwd=work, env=env, capture_output=True, check=False
            )
            self.assertNotEqual(branch_check.returncode, 0, branch_check.stderr)

    def test_publisher_uses_uv_attestations_without_running_build_code(self) -> None:
        jobs = self.workflow["jobs"]
        self.assertEqual(
            [name for name, job in jobs.items() if job.get("permissions", {}).get("id-token") == "write"], ["publish"]
        )
        publish = jobs["publish"]
        self.assertEqual(publish["environment"]["name"], "pypi")
        self.assertEqual(
            [s["name"] for s in publish["steps"]],
            [
                "Download release distributions",
                "Check release filenames",
                "Set up pinned uv",
                "Generate PEP 740 publish attestations",
                "Publish with required Trusted Publishing",
            ],
        )
        download, _, setup, attest, upload = publish["steps"]
        self.assertEqual(download["with"], {"name": "release-dist", "path": "dist"})
        self.assertEqual(setup["with"]["version"], "0.12.19")
        self.assertRegex(attest["uses"], r"^astral-sh/attest-action@[0-9a-f]{40}$")
        self.assertIn("dist/*.whl", attest["with"]["paths"])
        self.assertIn("dist/*.tar.gz", attest["with"]["paths"])
        self.assertIn("uv publish --no-config --trusted-publishing always", upload["run"])
        self.assertIn("https://upload.pypi.org/legacy/", upload["run"])
        self.assertFalse(any("actions/checkout" in s.get("uses", "") for s in publish["steps"]))

    def test_publisher_rejects_distributions_outside_release_tag(self) -> None:
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
