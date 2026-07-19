#!/usr/bin/env python3
"""Rebuild TestForge's Claude archives and release manifests deterministically."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "testforge"
VERSION = "1.1.0"
RELEASE_DATE = "2026-07-18"
SKILLS = ("software-verification", "verification-reviewer")
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
EXCLUDED = {"__pycache__", ".pytest_cache", ".git"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if b"\x00" in data:
        return data
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_record(path: Path, root: Path) -> dict[str, object]:
    data = canonical_bytes(path)
    return {
        "path": path.relative_to(root).as_posix(),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def files(root: Path, excluded_file: Path | None = None) -> list[Path]:
    result = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED for part in path.relative_to(root).parts):
            continue
        if excluded_file is not None and path.resolve() == excluded_file.resolve():
            continue
        result.append(path)
    return sorted(result, key=lambda path: path.relative_to(root).as_posix().lower())


def write_zip(source: Path, output: Path, top_level: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files(source):
            name = PurePosixPath(top_level, *path.relative_to(source).parts).as_posix()
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def write_manifest(root: Path, package_name: str) -> None:
    output = root / "release-manifest.json"
    artifacts = [canonical_record(path, root) for path in files(root, excluded_file=output)]
    manifest = {
        "format_version": "1.0",
        "package": package_name,
        "version": VERSION,
        "release_date": RELEASE_DATE,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "note": "release-manifest.json is excluded from its own hash list; UTF-8 text hashes use canonical LF line endings for cross-platform validation",
    }
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    archives = {}
    for skill in SKILLS:
        output = REPO / "claude-ai" / f"{skill}-v{VERSION}.zip"
        write_zip(PACKAGE / "skills" / skill, output, skill)
        archives[skill] = sha256(output)
    write_manifest(PACKAGE, "testforge")
    write_manifest(REPO, "testforge-public-repository")
    print(
        json.dumps(
            {
                "claude_zip_sha256": archives,
                "package_artifacts": json.loads((PACKAGE / "release-manifest.json").read_text(encoding="utf-8"))["artifact_count"],
                "repository_artifacts": json.loads((REPO / "release-manifest.json").read_text(encoding="utf-8"))["artifact_count"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
