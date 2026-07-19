#!/usr/bin/env python3
"""Validate TestForge release inventories and Claude archive parity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile
import zipfile


REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "testforge"
VERSION = "1.1.0"
SKILLS = ("software-verification", "verification-reviewer")
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


def files(root: Path, excluded_file: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.resolve() != excluded_file.resolve()
            and not any(part in EXCLUDED for part in path.relative_to(root).parts)
        ),
        key=lambda path: path.relative_to(root).as_posix().lower(),
    )


def validate_manifest(root: Path, expected_package: str) -> list[str]:
    errors = []
    manifest_path = root / "release-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid manifest {manifest_path}: {exc}"]
    actual = [canonical_record(path, root) for path in files(root, manifest_path)]
    if manifest.get("package") != expected_package:
        errors.append(f"unexpected package name in {manifest_path}")
    if manifest.get("version") != VERSION:
        errors.append(f"unexpected version in {manifest_path}")
    if manifest.get("artifact_count") != len(actual):
        errors.append(f"artifact count mismatch in {manifest_path}")
    if manifest.get("artifacts") != actual:
        errors.append(f"artifact inventory or hash mismatch in {manifest_path}")
    return errors


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in root.rglob("*")
        if path.is_file() and not any(part in EXCLUDED for part in path.relative_to(root).parts)
    }


def validate_archive(skill: str) -> list[str]:
    errors = []
    archive_path = REPO / "claude-ai" / f"{skill}-v{VERSION}.zip"
    if not zipfile.is_zipfile(archive_path):
        return [f"invalid Claude archive: {archive_path}"]
    with tempfile.TemporaryDirectory() as temporary:
        destination = Path(temporary)
        with zipfile.ZipFile(archive_path) as archive:
            names = [PurePosixPath(name.replace("\\", "/")) for name in archive.namelist() if name]
            if {name.parts[0] for name in names} != {skill}:
                errors.append(f"unexpected top-level folder in {archive_path}")
            if any(name.is_absolute() or ".." in name.parts for name in names):
                errors.append(f"unsafe member path in {archive_path}")
            archive.extractall(destination)
        if snapshot(PACKAGE / "skills" / skill) != snapshot(destination / skill):
            errors.append(f"archive content mismatch for {skill}")
    return errors


def main() -> int:
    errors = []
    errors.extend(validate_manifest(PACKAGE, "testforge"))
    errors.extend(validate_manifest(REPO, "testforge-public-repository"))
    for skill in SKILLS:
        errors.extend(validate_archive(skill))
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: release manifests, archive topology, and source parity match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
