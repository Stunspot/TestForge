import hashlib
from pathlib import Path, PurePosixPath
import tempfile
import unittest
import zipfile


REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "testforge"
CLAUDE = REPO / "claude-ai"
SKILLS = ("software-verification", "verification-reviewer")


def digest(path):
    value = hashlib.sha256()
    value.update(path.read_bytes())
    return value.hexdigest()


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


class HostPackagingTests(unittest.TestCase):
    def test_descriptions_fit_claude_limit(self):
        for skill in SKILLS:
            text = (PACKAGE / "skills" / skill / "SKILL.md").read_text(encoding="utf-8-sig")
            description = next(line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("description:"))
            self.assertLessEqual(len(description), 200, skill)

    def test_claude_archives_are_safe_and_match_source(self):
        for skill in SKILLS:
            archive_path = CLAUDE / f"{skill}-v1.1.1.zip"
            self.assertTrue(archive_path.is_file(), archive_path)
            with tempfile.TemporaryDirectory() as temporary:
                with zipfile.ZipFile(archive_path) as archive:
                    names = [PurePosixPath(name.replace("\\", "/")) for name in archive.namelist() if name]
                    self.assertEqual({name.parts[0] for name in names}, {skill})
                    self.assertTrue(all(not name.is_absolute() and ".." not in name.parts for name in names))
                    archive.extractall(temporary)
                self.assertEqual(snapshot(PACKAGE / "skills" / skill), snapshot(Path(temporary) / skill))


if __name__ == "__main__":
    unittest.main()
