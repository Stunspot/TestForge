import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.validate_release_manifests import canonical_bytes


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "testforge"
PLUGIN = ROOT / "plugins" / "testforge"
PLUGIN_SKILLS = PLUGIN / "skills"


class PublicDistributionTests(unittest.TestCase):
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

    def test_plugin_assets_and_skill_entrypoints_exist(self):
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        for key in ("composerIcon", "logo"):
            target = PLUGIN / manifest["interface"][key].removeprefix("./")
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


if __name__ == "__main__":
    unittest.main()
