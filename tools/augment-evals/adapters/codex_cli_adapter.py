from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence


class AdapterError(RuntimeError):
    pass


def resolve_codex_launcher(
    platform: str = os.name,
    which: Callable[[str], str | None] = shutil.which,
) -> str:
    candidates = ("codex.cmd", "codex.exe") if platform == "nt" else ("codex",)
    for candidate in candidates:
        resolved = which(candidate)
        if resolved:
            return resolved
    expected = " or ".join(candidates)
    raise AdapterError(f"Codex CLI launcher not found on PATH; expected {expected}")


def build_command(arguments: Sequence[str]) -> list[str]:
    if not arguments:
        raise AdapterError("Codex CLI adapter requires command arguments")
    return [resolve_codex_launcher(), *arguments]


def main(arguments: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    forwarded = list(arguments if arguments is not None else sys.argv[1:])
    prompt = sys.stdin.read()
    if "-" in forwarded and not prompt.strip():
        print("Codex CLI adapter received an empty prompt", file=sys.stderr)
        return 2

    try:
        completed = subprocess.run(
            build_command(forwarded),
            input=prompt or None,
            text=True,
            encoding="utf-8",
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=False,
        )
        return completed.returncode
    except (AdapterError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
