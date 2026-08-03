from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bootstrap_repository import (
    ATTRIBUTES,
    EDITORCONFIG,
    BootstrapError,
    bootstrap_repository,
    render_workflow,
)
REVISION = "0123456789abcdef0123456789abcdef01234567"


class BootstrapRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self):
        self.temporary.cleanup()

    def test_apply_bootstraps_fresh_repository_and_is_idempotent(self):
        result = bootstrap_repository(self.root, REVISION, apply=True)
        self.assertEqual("bootstrapped", result.status)
        self.assertEqual(
            [
                ".gitattributes",
                ".editorconfig",
                ".github/workflows/line-ending-policy.yml",
            ],
            result.changed_files,
        )
        self.assertEqual(ATTRIBUTES, (self.root / ".gitattributes").read_bytes())
        self.assertEqual(EDITORCONFIG, (self.root / ".editorconfig").read_bytes())
        self.assertNotIn(
            b"\r",
            (self.root / ".github/workflows/line-ending-policy.yml").read_bytes(),
        )
        self.assertEqual(
            "compliant",
            bootstrap_repository(self.root, REVISION, apply=True).status,
        )

    def test_check_mode_reports_without_writing(self):
        result = bootstrap_repository(self.root, REVISION)
        self.assertEqual("needs-bootstrap", result.status)
        self.assertFalse((self.root / ".gitattributes").exists())

    def test_existing_contract_is_never_overwritten(self):
        existing = b"* text eol=crlf\n"
        (self.root / ".gitattributes").write_bytes(existing)
        with self.assertRaisesRegex(BootstrapError, "existing contract differs"):
            bootstrap_repository(self.root, REVISION, apply=True)
        self.assertEqual(existing, (self.root / ".gitattributes").read_bytes())
        self.assertFalse((self.root / ".editorconfig").exists())

    def test_root_byte_custody_receives_only_the_gate(self):
        (self.root / ".gitattributes").write_bytes(b"* -text\n")
        result = bootstrap_repository(self.root, REVISION, apply=True)
        self.assertEqual("byte-custody", result.profile)
        self.assertEqual(
            [".github/workflows/line-ending-policy.yml"],
            result.changed_files,
        )
        self.assertFalse((self.root / ".editorconfig").exists())

    def test_action_revision_requires_a_full_commit_sha(self):
        with self.assertRaisesRegex(ValueError, "40-character"):
            render_workflow("main")


if __name__ == "__main__":
    unittest.main()
