"""Byte-policy regression checks; this does not qualify verification judgment."""
import sys,tempfile,unittest,zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import build_public_release as public
from rebuild_public_release import write_zip
from source_text_policy import assert_text_entries

class PackageTextPolicyTests(unittest.TestCase):
    def test_wrong_python_endings_leave_prior_archives_untouched(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent.resolve()) as tmp:
            root=Path(tmp);source=root/"source";source.mkdir();(source/"runtime.py").write_bytes(b"print('useful')\r\n")
            target=root/"accepted.zip";target.write_bytes(b"accepted bytes")
            for build in (lambda:public.zip_tree(source,target),lambda:write_zip(source,target,"skill")):
                with self.assertRaisesRegex(ValueError,"requires LF"):build()
                self.assertEqual(target.read_bytes(),b"accepted bytes")
    def test_lf_bytes_are_preserved_exactly(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent.resolve()) as tmp:
            root=Path(tmp);source=root/"source";source.mkdir();data=b"print('useful')\n";(source/"runtime.py").write_bytes(data)
            target=root/"candidate.zip";public.zip_tree(source,target)
            with zipfile.ZipFile(target) as z:self.assertEqual(z.read("runtime.py"),data)
    def test_windows_command_exception_is_specific(self):
        assert_text_entries([("Open.cmd",b"@echo off\r\n"),("asset.png",b"\r\n\x00")])
        with self.assertRaisesRegex(ValueError,"requires CRLF"):assert_text_entries([("Open.cmd",b"@echo off\n")])
        with self.assertRaisesRegex(ValueError,"requires LF"):assert_text_entries([("SKILL.md",b"# Task\r\n")])
    def test_public_build_checks_working_bytes_before_creating_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent.resolve()) as tmp:
            root=Path(tmp);(root/"plugins/testforge").mkdir(parents=True);(root/"release-docs").mkdir();(root/"plugins/testforge/SKILL.md").write_bytes(b"# Wrong\r\n")
            output=root/"releases/new"
            with patch.object(public,"ROOT",root),patch.object(public,"require_final_seal",return_value=SimpleNamespace(output_dir=output)):
                with self.assertRaisesRegex(ValueError,"requires LF"):public.main([])
            self.assertFalse(output.exists())
    def test_extensionless_text_is_checked_but_binary_is_preserved(self):
        with self.assertRaisesRegex(ValueError,"requires LF"):assert_text_entries([("NOTICE",b"notice\r\n")])
        assert_text_entries([("asset.bin",b"\x00\r\n")])

if __name__=="__main__":unittest.main()
