import os
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestReleaseTags(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "Release tag validation runs on Unix")
    def test_tag_formats(self) -> None:
        env = {key: value for key, value in os.environ.items() if key != "GITHUB_REF"}
        for tag, kind, valid in (
            ("v4.3.0", "ga", True),
            ("v5.0.0a1", "ga", False),
            ("v5.0.0b1", "ga", False),
            ("v4.3.0b1", "beta", True),
            ("v5.0.0b1", "beta", True),
            ("v5.0.0.dev1", "dev", True),
            ("v5.0.0.dev01", "dev", False),
            ("v5.0.0rc2", "rc", True),
            ("v5.0.0rc02", "rc", False),
            ("v4.3.0a69.post2", "preview", True),
            ("v4.3.0a69.2", "preview", False),
            ("v4.3.0a069.post02", "preview", False),
            ("v4.3.0a69.post2junk", "preview", False),
            ("v04.3.0", "ga", False),
            ("v4.3.0b01", "beta", False),
        ):
            with self.subTest(tag=tag):
                result = subprocess.run(
                    ["bash", ".github/workflows/validate_tag.sh", tag, kind],
                    cwd=REPO_ROOT,
                    env=env,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode == 0, valid, result.stdout + result.stderr)

    def test_publish_filename_check_accepts_all_kinds(self) -> None:
        workflow = (REPO_ROOT / ".github/workflows/python-tests.yml").read_text(encoding="utf-8")
        found = re.search(r're\.fullmatch\(r"(v[^"]+)", os\.environ\["GITHUB_REF_NAME"\]\)', workflow)
        self.assertIsNotNone(found)
        assert found is not None
        for tag in ("v4.3.0", "v4.3.0b1", "v5.0.0.dev1", "v5.0.0rc2", "v4.3.0a69.post2"):
            with self.subTest(tag=tag):
                self.assertTrue(re.fullmatch(found.group(1), tag))
