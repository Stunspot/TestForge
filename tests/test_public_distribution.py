import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.validate_release_manifests import canonical_bytes


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "testforge"
PLUGIN = ROOT / "plugins" / "testforge"
PLUGIN_SKILLS = PLUGIN / "skills"
PACKAGE_VERSION = "1.1.1"
PLUGIN_VERSION = "1.1.2"


class PublicDistributionTests(unittest.TestCase):
    def test_openai_submission_archive_is_reproducible_and_portal_shaped(self):
        tracked_archive = (
            ROOT
            / "release-assets"
            / "v1.1.2"
            / "Plugin-TestForge-v1.1.2-OpenAI-Submission.zip"
        )
        tracked_custody = (
            ROOT / "release-assets" / "v1.1.2" / "openai-submission-custody.json"
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / tracked_archive.name
            custody = Path(temporary) / "openai-submission-custody.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_openai_submission_archive.py"),
                    str(PLUGIN),
                    "--output",
                    str(output),
                    "--json-output",
                    str(custody),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(tracked_archive.read_bytes(), output.read_bytes())
            self.assertEqual(
                json.loads(tracked_custody.read_text(encoding="utf-8")),
                json.loads(custody.read_text(encoding="utf-8")),
            )

        with zipfile.ZipFile(tracked_archive) as archive:
            names = archive.namelist()
            self.assertTrue(names)
            self.assertTrue(all("\\" not in name for name in names))
            manifest = json.loads(
                archive.read("testforge-plugin/.codex-plugin/plugin.json").decode(
                    "utf-8"
                )
            )
            self.assertEqual({"composerIcon", "logo"}, set(manifest["interface"]))

    def test_release_hashes_are_line_ending_portable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            lf = root / "lf.md"
            crlf = root / "crlf.md"
            lf.write_bytes(b"one\ntwo\n")
            crlf.write_bytes(b"one\r\ntwo\r\n")
            self.assertEqual(canonical_bytes(lf), canonical_bytes(crlf))

    def test_marketplace_and_plugin_identity_agree(self):
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        entry = marketplace["plugins"][0]
        self.assertEqual("cd-testforge", marketplace["name"])
        self.assertEqual("testforge", entry["name"])
        self.assertEqual("./plugins/testforge", entry["source"]["path"])
        self.assertEqual(entry["name"], manifest["name"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertEqual(PLUGIN_VERSION, manifest["version"])
        package_manifest = (CANONICAL / "package-manifest.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"version: {PACKAGE_VERSION}\n", package_manifest)

        for prompt in manifest["interface"]["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128, prompt)

        for key in ("privacyPolicyURL", "termsOfServiceURL"):
            self.assertTrue(manifest["interface"][key].startswith("https://"))
        self.assertIn("DATA-AND-PRIVACY.md", manifest["interface"]["privacyPolicyURL"])
        self.assertIn("TERMS-OF-USE.md", manifest["interface"]["termsOfServiceURL"])

    def test_plugin_assets_and_skill_entrypoints_exist(self):
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        asset_paths = [manifest["interface"][key] for key in ("composerIcon", "logo")]
        asset_paths.extend(manifest["interface"].get("screenshots", []))
        for relative in asset_paths:
            target = PLUGIN / relative.removeprefix("./")
            self.assertTrue(target.is_file(), target)
            self.assertEqual(b"\x89PNG\r\n\x1a\n", target.read_bytes()[:8])
        for skill in ("software-verification", "verification-reviewer"):
            self.assertTrue((PLUGIN / "skills" / skill / "SKILL.md").is_file())
            self.assertTrue(
                (PLUGIN / "skills" / skill / "agents" / "openai.yaml").is_file()
            )

    def test_plugin_skills_are_byte_identical_to_canonical_skills(self):
        def inventory(root: Path):
            return {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }

        for skill in ("software-verification", "verification-reviewer"):
            self.assertEqual(
                inventory(CANONICAL / "skills" / skill),
                inventory(PLUGIN_SKILLS / skill),
            )

    def test_public_tree_has_no_cache_debris(self):
        tracked = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout.decode("utf-8").split("\0")
        debris = [
            path
            for path in tracked
            if path
            and (
                "__pycache__" in Path(path).parts
                or Path(path).suffix in {".pyc", ".pyo"}
            )
        ]
        self.assertEqual([], debris)

    def test_declared_customer_documents_exist(self):
        documentation = json.loads(
            (ROOT / "documentation-manifest.json").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(len(documentation["customer_docs"]), 17)
        for relative in documentation["customer_docs"]:
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
