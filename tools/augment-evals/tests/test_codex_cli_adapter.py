from __future__ import annotations

import importlib.util
import io
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "adapters" / "codex_cli_adapter.py"
SPEC = importlib.util.spec_from_file_location("codex_cli_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class LauncherResolutionTests(unittest.TestCase):
    def test_windows_prefers_cmd_launcher_over_extensionless_or_packaged_aliases(self):
        seen: list[str] = []

        def which(name: str) -> str | None:
            seen.append(name)
            return r"D:\npm-global\codex.cmd" if name == "codex.cmd" else None

        resolved = adapter.resolve_codex_launcher("nt", which)

        self.assertEqual(r"D:\npm-global\codex.cmd", resolved)
        self.assertEqual(["codex.cmd"], seen)

    def test_windows_can_fall_back_to_an_accessible_standalone_executable(self):
        found = {
            "codex.cmd": None,
            "codex.exe": r"C:\Tools\Codex\codex.exe",
        }

        resolved = adapter.resolve_codex_launcher("nt", found.get)

        self.assertEqual(r"C:\Tools\Codex\codex.exe", resolved)

    def test_non_windows_uses_native_codex_command(self):
        resolved = adapter.resolve_codex_launcher(
            "posix", lambda name: "/usr/local/bin/codex" if name == "codex" else None
        )

        self.assertEqual("/usr/local/bin/codex", resolved)

    def test_missing_launcher_fails_with_platform_specific_message(self):
        with self.assertRaisesRegex(adapter.AdapterError, "codex.cmd or codex.exe"):
            adapter.resolve_codex_launcher("nt", lambda _name: None)


class ForwardingTests(unittest.TestCase):
    def test_main_forwards_utf8_prompt_and_returns_child_status(self):
        stdin = io.StringIO("Evaluate the fictional package.")
        stdout = io.StringIO()
        stderr = io.StringIO()
        completed = subprocess.CompletedProcess([], 7)

        with (
            patch.object(adapter.sys, "stdin", stdin),
            patch.object(adapter.sys, "stdout", stdout),
            patch.object(adapter.sys, "stderr", stderr),
            patch.object(adapter, "resolve_codex_launcher", return_value=r"D:\npm-global\codex.cmd"),
            patch.object(adapter.subprocess, "run", return_value=completed) as run,
        ):
            status = adapter.main(["exec", "--ephemeral", "-"])

        self.assertEqual(7, status)
        self.assertEqual(
            [r"D:\npm-global\codex.cmd", "exec", "--ephemeral", "-"],
            run.call_args.args[0],
        )
        self.assertEqual("Evaluate the fictional package.", run.call_args.kwargs["input"])
        self.assertEqual("utf-8", run.call_args.kwargs["encoding"])
        self.assertFalse(run.call_args.kwargs["check"])

    def test_empty_stdin_is_rejected_when_dash_requests_prompt_input(self):
        with (
            patch.object(adapter.sys, "stdin", io.StringIO("")),
            patch.object(adapter.sys, "stdout", io.StringIO()),
            patch.object(adapter.sys, "stderr", io.StringIO()),
            patch.object(adapter.subprocess, "run") as run,
        ):
            status = adapter.main(["exec", "-"])

        self.assertEqual(2, status)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
