#!/usr/bin/env python3
"""Install TestForge's canonical line-ending policy in a Git repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


COMMIT_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
WORKFLOW_PATH = Path(".github/workflows/line-ending-policy.yml")

ATTRIBUTES = """* text=auto eol=lf

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
*.webp binary
*.mp4 binary
""".encode("utf-8")

EDITORCONFIG = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true

[*.{bat,cmd}]
end_of_line = crlf
""".encode("utf-8")


class BootstrapError(RuntimeError):
    """Raised when bootstrap would overwrite an existing repository contract."""


@dataclass
class BootstrapResult:
    root: str
    status: str
    profile: str
    changed_files: list[str]
    detail: str = ""


def render_workflow(action_revision: str) -> bytes:
    if not COMMIT_SHA.fullmatch(action_revision):
        raise ValueError("action revision must be a full 40-character Git commit SHA")
    return f"""name: Line ending policy

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  line-ending-policy:
    name: line-ending-policy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: Stunspot/testforge/line-ending-policy@{action_revision.lower()}
""".encode("utf-8")


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.testforge-{os.getpid()}.tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def planned_file(path: Path, expected: bytes) -> bool:
    if not path.exists():
        return True
    if normalized(path.read_bytes()) != expected:
        raise BootstrapError(f"existing contract differs: {path.name}")
    return path.read_bytes() != expected


def bootstrap_repository(
    root: Path,
    action_revision: str,
    apply: bool = False,
) -> BootstrapResult:
    root = root.resolve()
    if not root.is_dir():
        raise BootstrapError(f"repository root is not a directory: {root}")
    if not (root / ".git").exists():
        raise BootstrapError(f"repository root is not initialized: {root}")

    workflow = render_workflow(action_revision)
    attributes_path = root / ".gitattributes"
    editorconfig_path = root / ".editorconfig"
    workflow_path = root / WORKFLOW_PATH

    existing_attributes = (
        normalized(attributes_path.read_bytes()) if attributes_path.exists() else None
    )
    byte_custody = existing_attributes == b"* -text\n"
    profile = "byte-custody" if byte_custody else "standard"

    changes: list[tuple[Path, bytes]] = []
    if not byte_custody and planned_file(attributes_path, ATTRIBUTES):
        changes.append((attributes_path, ATTRIBUTES))
    if not byte_custody and planned_file(editorconfig_path, EDITORCONFIG):
        changes.append((editorconfig_path, EDITORCONFIG))
    if planned_file(workflow_path, workflow):
        changes.append((workflow_path, workflow))

    changed_files = [path.relative_to(root).as_posix() for path, _data in changes]
    if not changes:
        return BootstrapResult(str(root), "compliant", profile, [])
    if not apply:
        return BootstrapResult(
            str(root),
            "needs-bootstrap",
            profile,
            changed_files,
            "rerun with --apply",
        )

    for path, data in changes:
        atomic_write(path, data)
    return BootstrapResult(str(root), "bootstrapped", profile, changed_files)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install TestForge's canonical line-ending policy and CI gate."
    )
    parser.add_argument("root", type=Path)
    parser.add_argument("--action-revision", required=True)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = bootstrap_repository(
            args.root,
            args.action_revision,
            apply=args.apply,
        )
        payload = asdict(result)
    except (BootstrapError, OSError, ValueError) as error:
        payload = {
            "root": str(args.root.resolve()),
            "status": "conflict",
            "profile": "unknown",
            "changed_files": [],
            "detail": str(error),
        }
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0 if payload["status"] in {"compliant", "bootstrapped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
