from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from verify_line_endings import verify as verify_line_endings


STANDARD_ATTRIBUTES = """* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.zip binary
*.docx binary
*.xlsx binary
*.pptx binary
*.pdf binary
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
"""

STANDARD_EDITORCONFIG = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true

[*.{bat,cmd}]
end_of_line = crlf
"""


class LineEndingPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self):
        self.temporary.cleanup()

    def git_add(self, *paths: str):
        subprocess.run(
            ["git", "-c", "core.autocrlf=false", "add", *paths],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def add_raw_blob(self, path: str, data: bytes):
        object_id = subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=self.root,
            check=True,
            capture_output=True,
            input=data,
        ).stdout.decode("ascii").strip()
        subprocess.run(
            ["git", "update-index", "--add", "--cacheinfo", f"100644,{object_id},{path}"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def write_standard_policy(self):
        (self.root / ".gitattributes").write_text(STANDARD_ATTRIBUTES, encoding="utf-8", newline="\n")
        (self.root / ".editorconfig").write_text(STANDARD_EDITORCONFIG, encoding="utf-8", newline="\n")

    def test_standard_policy_passes_effective_and_blob_checks(self):
        self.write_standard_policy()
        (self.root / "README.md").write_bytes(b"one\ntwo\n")
        self.git_add(".")
        result = verify_line_endings(self.root)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("standard", result["profile"])
        self.assertEqual([], result["indexed_text_cr_paths"])

    def test_missing_windows_and_binary_rules_fail_effective_probes(self):
        (self.root / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
        (self.root / ".editorconfig").write_text(STANDARD_EDITORCONFIG, encoding="utf-8")
        self.git_add(".")
        result = verify_line_endings(self.root)
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(any(item["code"] == "ATTRIBUTE_MISMATCH" for item in result["findings"]))

    def test_crlf_already_in_index_is_rejected(self):
        (self.root / "bad.txt").write_bytes(b"one\r\ntwo\r\n")
        self.add_raw_blob("bad.txt", b"one\r\ntwo\r\n")
        self.write_standard_policy()
        self.git_add(".gitattributes", ".editorconfig")
        result = verify_line_endings(self.root)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(["bad.txt"], result["indexed_text_cr_paths"])

    def test_scoped_byte_custody_exempts_canonical_cr_bytes(self):
        self.write_standard_policy()
        with (self.root / ".gitattributes").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write("/release/** -text\n")
        release = self.root / "release"
        release.mkdir()
        (release / "receipt.md").write_bytes(b"one\r\ntwo\r\n")
        self.git_add(".")
        result = verify_line_endings(self.root)
        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["indexed_text_cr_paths"])

    def test_gitlink_is_not_scanned_as_a_blob(self):
        commit = (
            b"tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904\n"
            b"author Test <test@example.com> 0 +0000\n"
            b"committer Test <test@example.com> 0 +0000\n"
            b"\nsubmodule fixture\n"
        )
        object_id = subprocess.run(
            ["git", "hash-object", "-t", "commit", "-w", "--stdin"],
            cwd=self.root,
            check=True,
            capture_output=True,
            input=commit,
        ).stdout.decode("ascii").strip()
        subprocess.run(
            [
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{object_id},vendor/example",
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        self.write_standard_policy()
        self.git_add(".gitattributes", ".editorconfig")
        result = verify_line_endings(self.root)
        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["indexed_text_cr_paths"])

    def test_root_byte_custody_is_a_separate_passing_profile(self):
        (self.root / ".gitattributes").write_text("* -text\n", encoding="utf-8")
        (self.root / "canonical.bin").write_bytes(b"one\r\ntwo\r\n")
        self.git_add(".")
        result = verify_line_endings(self.root)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("byte-custody", result["profile"])


if __name__ == "__main__":
    unittest.main()
