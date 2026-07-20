#!/usr/bin/env python3
"""Build TestForge's deterministic release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--package-name", default="testforge")
    parser.add_argument("--version", default="1.1.1")
    parser.add_argument("--release-date", default="2026-07-18")
    args = parser.parse_args()
    root = args.package.resolve()
    output = root / "release-manifest.json"
    artifacts = []
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file()
        and item != output
        and ".git" not in item.relative_to(root).parts
        and "__pycache__" not in item.relative_to(root).parts
    ):
        artifacts.append({
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": digest(path),
        })
    manifest = {
        "format_version": "1.0",
        "package": args.package_name,
        "version": args.version,
        "release_date": args.release_date,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "note": "release-manifest.json is excluded from its own hash list",
    }
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
