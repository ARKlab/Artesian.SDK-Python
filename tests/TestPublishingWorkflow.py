import base64
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import unquote

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/python-tests.yml"


class TestPublishingWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow_text = WORKFLOW.read_text()
        cls.workflow = yaml.safe_load(cls.workflow_text)
        cls.publish = cls.workflow["jobs"]["publish"]
        cls.steps = {step["name"]: step for step in cls.publish["steps"]}

    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix=".publishing-test-", dir=".")
        self.addCleanup(directory.cleanup)
        previous = Path.cwd()
        self.addCleanup(os.chdir, previous)
        os.chdir(directory.name)
        Path("dist").mkdir()
        self.env = {
            "SOURCE_SHA": "a" * 40,
            "GITHUB_SHA": "b" * 40,
            "GITHUB_WORKFLOW_SHA": "d" * 40,
            "GITHUB_RUN_ID": "67890",
            "GITHUB_RUN_ATTEMPT": "2",
            "ARTIFACT_ID": "12345",
            "ARTIFACT_DIGEST": "c" * 64,
            "GITHUB_STEP_SUMMARY": str(Path("summary").resolve()),
        }
        self.urlopen = self.enter_patch("urllib.request.urlopen", side_effect=AssertionError("No real network"))
        self.sleep = self.enter_patch("time.sleep")
        self.make_distributions()

    def enter_patch(self, target, **kwargs):
        patcher = patch(target, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def run_step(self, name):
        step = self.steps[name]
        self.assertEqual(step["shell"], "python")
        with patch.dict(os.environ, self.env, clear=True):
            exec(compile(step["run"], f"{WORKFLOW}:{name}", "exec"), {})

    def make_distributions(self, tag="v4.3.0", version="4.3.0"):
        for path in Path("dist").iterdir():
            path.unlink()
        self.env["GITHUB_REF_NAME"] = tag
        self.files = {}
        for name, content, key in (
            (f"artesian_sdk-{version}-py3-none-any.whl", b"wheel bytes", "WHEEL_SHA"),
            (f"artesian_sdk-{version}.tar.gz", b"sdist bytes", "SDIST_SHA"),
        ):
            (Path("dist") / name).write_bytes(content)
            self.files[name] = self.env[key] = hashlib.sha256(content).hexdigest()

    def attestation(self, name, digest, **statement_fields):
        statement = {
            "_type": "https://in-toto.io/Statement/v1",
            "predicateType": "https://docs.pypi.org/attestations/publish/v1",
            "subject": [{"name": name, "digest": {"sha256": digest}}],
            "predicate": {},
        }
        statement.update(statement_fields)
        return {
            "version": 1,
            "envelope": {
                "statement": base64.b64encode(json.dumps(statement).encode()).decode(),
                "signature": base64.b64encode(b"dummy signature").decode(),
            },
            "verification_material": {
                "certificate": base64.b64encode(b"dummy certificate").decode(),
                "transparency_entries": [{"logIndex": 1}],
            },
        }

    def write_sidecars(self):
        self.run_step("Validate distribution identity")
        for name, digest in self.files.items():
            (Path("dist") / (name + ".publish.attestation")).write_text(json.dumps(self.attestation(name, digest)))

    def provenance(self, name):
        return {
            "version": 1,
            "attestation_bundles": [
                {
                    "publisher": {
                        "kind": "GitHub",
                        "repository": "ARKlab/Artesian.SDK-Python",
                        "workflow": "python-tests.yml",
                        "environment": "pypi",
                    },
                    "attestations": [self.attestation(name, self.files[name])],
                }
            ],
        }

    def response(self, request, **kwargs):
        name = unquote(request.full_url.split("/")[-2])
        return io.BytesIO(json.dumps(self.provenance(name)).encode())

    def test_release_versions_and_build_identity(self):
        for tag, version in (
            ("v4.3.0", "4.3.0"),
            ("v4.3.0b2", "4.3.0b2"),
            ("v4.3.0a69.2", "4.3.0a69.post2"),
            ("v04.03.00", "4.3.0"),
            ("v04.03.00b02", "4.3.0b2"),
            ("v04.03.00a069.02", "4.3.0a69.post2"),
        ):
            with self.subTest(tag=tag):
                self.make_distributions(tag, version)
                self.run_step("Validate distribution identity")
                record = json.loads(Path("release.json").read_text())
                self.assertEqual(
                    record,
                    {
                        "version": version,
                        "source_sha": self.env["SOURCE_SHA"],
                        "trigger_sha": self.env["GITHUB_SHA"],
                        "workflow_sha": self.env["GITHUB_WORKFLOW_SHA"],
                        "run_id": self.env["GITHUB_RUN_ID"],
                        "run_attempt": self.env["GITHUB_RUN_ATTEMPT"],
                        "artifact_id": self.env["ARTIFACT_ID"],
                        "artifact_digest": self.env["ARTIFACT_DIGEST"],
                        "files": self.files,
                    },
                )
                self.assertNotEqual(record["source_sha"], record["trigger_sha"])
                self.assertIn(json.dumps(record, indent=2), Path("summary").read_text())

    def test_identity_rejects_extra_files_including_supplied_attestations(self):
        for extra in ("untrusted.py", next(iter(self.files)) + ".publish.attestation"):
            with self.subTest(extra=extra):
                path = Path("dist") / extra
                path.write_text("{}")
                with self.assertRaises(SystemExit):
                    self.run_step("Validate distribution identity")
                path.unlink()

    def test_identity_rejects_missing_or_tampered_distributions(self):
        for name in self.files:
            for missing in (True, False):
                with self.subTest(name=name, missing=missing):
                    self.make_distributions()
                    path = Path("dist") / name
                    if missing:
                        path.unlink()
                    else:
                        path.write_bytes(b"tampered")
                    with self.assertRaises(SystemExit):
                        self.run_step("Validate distribution identity")

    def test_identity_rejects_invalid_tag_and_build_outputs(self):
        for key, value in (
            ("GITHUB_REF_NAME", "v4.3.0rc1"),
            ("SOURCE_SHA", ""),
            ("SOURCE_SHA", "z" * 40),
            ("ARTIFACT_DIGEST", ""),
            ("ARTIFACT_DIGEST", "z" * 64),
            ("ARTIFACT_ID", ""),
            ("ARTIFACT_ID", "artifact-name"),
            ("WHEEL_SHA", "0" * 64),
            ("SDIST_SHA", "0" * 64),
        ):
            with self.subTest(key=key, value=value), patch.dict(self.env, {key: value}):
                with self.assertRaises(SystemExit):
                    self.run_step("Validate distribution identity")

    def test_local_check_matches_shape_not_cryptographic_signatures(self):
        # Dummy signatures/certificates deliberately pass: PyPI verifies cryptography.
        self.write_sidecars()
        self.run_step("Require matching attestations")

    def test_local_check_rejects_missing_sidecars_and_tampering(self):
        for name in self.files:
            for missing in (True, False):
                with self.subTest(name=name, missing=missing):
                    self.make_distributions()
                    self.write_sidecars()
                    if missing:
                        (Path("dist") / (name + ".publish.attestation")).unlink()
                    else:
                        (Path("dist") / name).write_bytes(b"changed after signing")
                    with self.assertRaises(SystemExit):
                        self.run_step("Require matching attestations")

    def test_local_check_rejects_mismatched_statements_and_invalid_json(self):
        name, digest = next(iter(self.files.items()))
        for fields in (
            {"subject": [{"name": "wrong.whl", "digest": {"sha256": digest}}]},
            {"subject": [{"name": name, "digest": {"sha256": "0" * 64}}]},
            {"_type": "wrong"},
            {"predicateType": "wrong"},
            None,
        ):
            with self.subTest(fields=fields):
                self.make_distributions()
                self.write_sidecars()
                sidecar = Path("dist") / (name + ".publish.attestation")
                sidecar.write_text("{" if fields is None else json.dumps(self.attestation(name, digest, **fields)))
                with self.assertRaises((SystemExit, json.JSONDecodeError)):
                    self.run_step("Require matching attestations")

    def test_pypi_verifies_both_files_and_exact_endpoint(self):
        self.run_step("Validate distribution identity")
        self.urlopen.side_effect = self.response
        self.run_step("Verify PyPI attestation availability")
        self.assertEqual(self.urlopen.call_count, 2)
        for call, name in zip(self.urlopen.call_args_list, self.files):
            request = call.args[0]
            self.assertEqual(request.full_url, f"https://pypi.org/integrity/artesian-sdk/4.3.0/{name}/provenance")
            self.assertEqual(request.get_header("Accept"), "application/vnd.pypi.integrity.v1+json")
            self.assertEqual(call.kwargs["timeout"], 30)
            self.assertIn(name, Path("summary").read_text())
        self.sleep.assert_not_called()

    def test_pypi_retries_then_fails_closed(self):
        self.run_step("Validate distribution identity")
        name = next(iter(self.files))
        for invalid in ("kind", "repository", "workflow", "environment", "digest", "empty", "404"):
            with self.subTest(invalid=invalid):

                def response(request, **kwargs):
                    if invalid == "404":
                        raise HTTPError(request.full_url, 404, "Not Found", {}, None)
                    provenance = self.provenance(name)
                    bundle = provenance["attestation_bundles"][0]
                    if invalid == "empty":
                        provenance["attestation_bundles"] = []
                    elif invalid == "digest":
                        bundle["attestations"] = [self.attestation(name, "0" * 64)]
                    else:
                        bundle["publisher"][invalid] = "wrong"
                    return io.BytesIO(json.dumps(provenance).encode())

                self.urlopen.reset_mock()
                self.sleep.reset_mock()
                self.urlopen.side_effect = response
                with self.assertRaisesRegex(SystemExit, "no matching publish attestation"):
                    self.run_step("Verify PyPI attestation availability")
                self.assertEqual(self.urlopen.call_count, 6)
                self.assertEqual(self.sleep.call_count, 5)

    def test_pypi_requires_second_file_to_verify(self):
        self.run_step("Validate distribution identity")
        first = next(iter(self.files))

        def response(request, **kwargs):
            if first in request.full_url:
                return self.response(request)
            return io.BytesIO(b'{"version": 1, "attestation_bundles": []}')

        self.urlopen.side_effect = response
        with self.assertRaises(SystemExit):
            self.run_step("Verify PyPI attestation availability")
        self.assertEqual(self.urlopen.call_count, 7)

    def test_pypi_404_then_valid_succeeds(self):
        self.run_step("Validate distribution identity")
        self.urlopen.side_effect = [
            HTTPError("https://pypi.org/", 404, "Not Found", {}, None),
            *(io.BytesIO(json.dumps(self.provenance(name)).encode()) for name in self.files),
        ]
        self.run_step("Verify PyPI attestation availability")
        self.assertEqual(self.urlopen.call_count, 3)
        self.sleep.assert_called_once_with(10)

    def test_only_isolated_publish_job_can_use_oidc(self):
        self.assertNotEqual(self.workflow.get("permissions", {}).get("id-token"), "write")
        writers = [
            name for name, job in self.workflow["jobs"].items() if job.get("permissions", {}).get("id-token") == "write"
        ]
        self.assertEqual(writers, ["publish"])
        self.assertEqual(self.publish["environment"]["name"], "pypi")
        self.assertNotIn("PYPI_API_TOKEN", self.workflow_text)
        for step in self.publish["steps"]:
            self.assertNotIn("actions/checkout", step.get("uses", ""))
            self.assertNotRegex(step.get("run", ""), r"\b(?:uv\s+(?:build|sync)|pip\s+install|python\s+-m\s+build)\b")
        download = self.steps["Download validated distributions"]["with"]
        self.assertEqual(download["artifact-ids"], "${{ env.ARTIFACT_ID }}")
        self.assertNotIn("name", download)
        self.assertNotIn("pattern", download)
        self.assertRegex(
            self.steps["Generate PEP 740 publish attestations"]["uses"], r"^astral-sh/attest-action@[0-9a-f]{40}$"
        )
        publish = self.steps["Publish with required Trusted Publishing"]["run"]
        self.assertIn("--trusted-publishing always", publish)
        self.assertNotIn("--no-attestations", publish)
        retain = self.steps["Retain release identity and signed distributions"]
        self.assertIn("always()", retain["if"])
        self.assertIn("steps.identity.outcome == 'success'", retain["if"])
        self.assertIn("dist/", retain["with"]["path"])
        self.assertIn("release.json", retain["with"]["path"])
        names = list(self.steps)
        ordered = [
            "Validate distribution identity",
            "Generate PEP 740 publish attestations",
            "Require matching attestations",
            "Publish with required Trusted Publishing",
            "Verify PyPI attestation availability",
            "Retain release identity and signed distributions",
        ]
        self.assertEqual([name for name in names if name in ordered], ordered)

    def test_build_outputs_and_mutually_exclusive_producers(self):
        producers = ["build-stable", "build-beta", "build-preview"]
        self.assertEqual(set(self.publish["needs"]), set(producers))
        condition = self.publish["if"]
        self.assertIn("!cancelled()", condition)
        self.assertIn("github.event_name == 'push'", condition)
        quality_runs = "\n".join(step.get("run", "") for step in self.workflow["jobs"]["quality"]["steps"])
        self.assertIn("twine check dist/*", quality_runs)
        for producer in producers:
            clause = f"needs.{producer}.result == 'success'"
            for other in producers:
                if other != producer:
                    clause += f" && needs.{other}.result == 'skipped'"
            self.assertIn(f"({clause})", condition)
            build = self.workflow["jobs"][producer]
            steps = {step["name"]: step for step in build["steps"]}
            names = list(steps)
            self.assertLess(names.index("Record release source"), names.index("Build package"))
            self.assertLess(names.index("Check release metadata"), names.index("Upload release distributions"))
            self.assertIn("twine check dist/*", steps["Check release metadata"]["run"])
            self.assertIn("git rev-parse HEAD", steps["Record release source"]["run"])
            self.assertIn('>> "$GITHUB_OUTPUT"', steps["Record release source"]["run"])
            hashes = steps["Record distribution hashes"]["run"]
            self.assertIn('Source commit: ${{ steps.source.outputs.sha }}" >> "$GITHUB_STEP_SUMMARY"', hashes)
            self.assertIn('sha256sum dist/*.whl dist/*.tar.gz >> "$GITHUB_STEP_SUMMARY"', hashes)
            self.assertEqual(build["outputs"]["source-sha"], "${{ steps.source.outputs.sha }}")
            for key in ("artifact-id", "artifact-digest"):
                self.assertEqual(build["outputs"][key], "${{ steps.distributions.outputs." + key + " }}")
            for key, env_key, pattern in (("wheel-sha", "WHEEL_SHA", "*.whl"), ("sdist-sha", "SDIST_SHA", "*.tar.gz")):
                self.assertEqual(build["outputs"][key], "${{ steps.hashes.outputs." + key + " }}")
                self.assertIn(f"{key}=$(sha256sum dist/{pattern}", steps["Record distribution hashes"]["run"])
                output_line = next(line for line in hashes.splitlines() if f"{key}=$(" in line)
                self.assertIn('>> "$GITHUB_OUTPUT"', output_line)
                self.assertIn(f"needs.{producer}.outputs.{key}", self.publish["env"][env_key])
            for key in ("source-sha", "artifact-id", "artifact-digest"):
                self.assertIn(f"needs.{producer}.outputs.{key}", self.publish["env"][key.upper().replace("-", "_")])
