import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = "1.1.1"
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class DocumentationCurrencyTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(
            (ROOT / "documentation-manifest.json").read_text(encoding="utf-8")
        )

    def test_customer_document_manifest_is_complete_and_coherent(self):
        documents = self.manifest["customer_docs"]
        self.assertEqual(len(documents), len(set(documents)))
        self.assertEqual(19, len(documents))
        self.assertIn("testforge/docs/TERMS-OF-USE.md", documents)
        self.assertIn("ARCHIVE-CUSTODY.md", documents)
        self.assertIn(f"RELEASE-NOTES-v{CURRENT_VERSION}.md", documents)

        declared = set(documents)
        for moment, paths in self.manifest["moments"].items():
            self.assertTrue(paths, moment)
            for relative in paths:
                self.assertIn(relative, declared, f"{moment}: {relative}")
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_current_customer_paths_use_current_release_identity(self):
        expected = {
            "README.md": [f"v{CURRENT_VERSION}"],
            "testforge/docs/HOST-COMPATIBILITY.md": [
                f"v{CURRENT_VERSION}",
                f"software-verification-v{CURRENT_VERSION}.zip",
                f"verification-reviewer-v{CURRENT_VERSION}.zip",
            ],
            "testforge/docs/INSTALL-CLAUDE.md": [
                f"software-verification-v{CURRENT_VERSION}.zip",
                f"verification-reviewer-v{CURRENT_VERSION}.zip",
            ],
            "testforge/docs/QUICK-START.md": [f"v{CURRENT_VERSION}"],
            "testforge/docs/DATA-AND-PRIVACY.md": [f"v{CURRENT_VERSION}"],
            f"RELEASE-NOTES-v{CURRENT_VERSION}.md": [f"v{CURRENT_VERSION}"],
        }
        for relative, required in expected.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for value in required:
                self.assertIn(value, text, f"{relative}: {value}")

        customer_text = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in self.manifest["customer_docs"]
        ).lower()
        self.assertNotIn("once published", customer_text)

    def test_all_tracked_markdown_local_links_resolve(self):
        tracked = subprocess.run(
            ["git", "ls-files", "*.md"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.splitlines()
        broken = []
        for relative in tracked:
            source = ROOT / relative
            text = source.read_text(encoding="utf-8")
            for raw_target in LINK_PATTERN.findall(text):
                target = raw_target.strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                if target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                    continue
                target = unquote(target.split("#", 1)[0].strip())
                if not target:
                    continue
                if " " in target and not target.startswith(("./", "../")):
                    target = target.split(" ", 1)[0]
                resolved = (source.parent / target).resolve()
                if not resolved.exists():
                    broken.append(f"{relative} -> {raw_target}")
        self.assertEqual([], broken)


if __name__ == "__main__":
    unittest.main()
