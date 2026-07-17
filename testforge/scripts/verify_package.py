#!/usr/bin/env python3
"""Verify package structure, machine-readable assets, Python syntax, and skill paths."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from common.filesystem import iter_files, write_json

REQUIRED = [
    "README.md", "LICENSE.md", "SECURITY.md", "package-manifest.yaml",
    "skills/software-verification/SKILL.md", "skills/verification-reviewer/SKILL.md",
    "assets/schemas/verification-manifest.schema.json", "assets/templates/verification-manifest.json",
    "scripts/validate_manifest.py", "scripts/validate_traceability.py", "scripts/normalize_test_results.py",
    "examples/typescript-api-change/walkthrough.md", "examples/python-regression/walkthrough.md", "examples/parser-edge-cases/walkthrough.md",
    "fallback/master-prompt.md", "evals/eval-manifest.yaml",
]
PRIVATE_PATH = re.compile(
    r"(?:[A-Za-z]:\\+(?:Users\\+|Github\\+cd-augment-lab|Indranet)|/Users/|/home/[^/]+/)",
    re.IGNORECASE,
)
RELATIVE_LINK = re.compile(r"`((?:\.\./)+[^`]+)`")


def verify(root: Path) -> dict:
    root = root.resolve(); errors: list[str] = []; warnings: list[str] = []; checked = 0
    for rel in REQUIRED:
        if not (root / rel).is_file(): errors.append(f"missing required file: {rel}")
    for path in iter_files(root):
        checked += 1
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() == ".json":
            try: json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as exc: errors.append(f"invalid JSON {rel}: {exc}")
        if path.suffix.lower() == ".py":
            try: compile(path.read_text(encoding="utf-8-sig"), str(path), "exec")
            except (OSError, SyntaxError) as exc: errors.append(f"invalid Python {rel}: {exc}")
        if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json", ".py"}:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            if path.name != "verify_package.py" and PRIVATE_PATH.search(text): errors.append(f"private absolute path found in {rel}")
            if path.name == "SKILL.md":
                if not text.startswith("---\n") or "\nname:" not in text[:1000] or "\ndescription:" not in text[:2000]: errors.append(f"invalid skill envelope: {rel}")
                for raw in RELATIVE_LINK.findall(text):
                    clean = raw.split("#", 1)[0]
                    candidate = (path.parent / clean).resolve()
                    if not candidate.exists(): errors.append(f"broken skill resource path in {rel}: {raw}")
    return {"valid": not errors, "root": str(root), "files_checked": checked, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(); report = verify(args.package)
    if args.output: write_json(args.output, report)
    else: print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
