#!/usr/bin/env python3
"""Verify one extracted settled-family release without host-specific dependencies."""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_DOCS = {
    "README.md", "QUICK-START.md", "INSTALL-CODEX.md", "INSTALL-CLAUDE.md",
    "CAPABILITIES.md", "LIMITATIONS.md", "SUPPORT.md", "VALIDATION.md",
    "MAINTAINER-GUIDE.md", "PACKAGE-REFERENCE.md", "DESCRIPTION-CUSTODY.md",
    "PROVENANCE.md", "HOST-EVIDENCE-BOUNDARY.md",
}
PRIVATE_TOPOLOGY_PATTERN = re.compile(
    r"(?i)(?:C:[\\/]+Users[\\/]+user(?:[\\/]+|$)|E:[\\/]+(?:Github|Indranet)(?:[\\/]+|$))"
)
SCHEMA = "cd-family-release-portable-verification/v1"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_member_name(name: str) -> bool:
    if not isinstance(name, str) or not name or "\\" in name or "\x00" in name:
        return False
    trimmed = name[:-1] if name.endswith("/") else name
    if not trimmed:
        return False
    parts = trimmed.split("/")
    return all(part and part not in {".", ".."} and ":" not in part for part in parts)


def safe_component(value: object) -> bool:
    return isinstance(value, str) and safe_member_name(value) and "/" not in value


def text_has_private_topology(data: bytes) -> bool:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return PRIVATE_TOPOLOGY_PATTERN.search(text) is not None


def read_json(path: Path, findings: list[str], label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        findings.append(f"{label}: invalid or missing JSON: {error}")
        return {}
    if not isinstance(value, dict):
        findings.append(f"{label}: JSON root must be an object")
        return {}
    return value


def inspect_zip_bytes(
    data: bytes, label: str, findings: list[str], seen: set[str], depth: int = 0,
) -> int:
    digest = sha256_bytes(data)
    if digest in seen:
        return 0
    seen.add(digest)
    if depth > 4:
        findings.append(f"{label}: nested ZIP depth exceeds 4")
        return 0
    members = 0
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            if len({name.casefold() for name in names}) != len(names):
                findings.append(f"{label}: ZIP has duplicate or case-colliding members")
            for info in archive.infolist():
                members += 1
                if not safe_member_name(info.filename):
                    findings.append(f"{label}: unsafe ZIP member: {info.filename}")
                if info.flag_bits & 0x1:
                    findings.append(f"{label}: encrypted ZIP member: {info.filename}")
                if ((info.external_attr >> 16) & 0o170000) == 0o120000:
                    findings.append(f"{label}: symlink ZIP member: {info.filename}")
                try:
                    member_data = archive.read(info)
                except (RuntimeError, zipfile.BadZipFile) as error:
                    findings.append(f"{label}: unreadable ZIP member {info.filename}: {error}")
                    continue
                if text_has_private_topology(member_data):
                    findings.append(f"{label}: private topology in ZIP member: {info.filename}")
                if zipfile.is_zipfile(io.BytesIO(member_data)):
                    members += inspect_zip_bytes(
                        member_data, f"{label}!{info.filename}", findings, seen, depth + 1
                    )
    except zipfile.BadZipFile as error:
        findings.append(f"{label}: invalid ZIP: {error}")
    return members


def verify(root: Path) -> dict[str, Any]:
    root = root.resolve()
    findings: list[str] = []
    manifest = read_json(root / "manifest.json", findings, "manifest")
    if manifest.get("schema") != "cd-settled-family-release/v1":
        findings.append("manifest: unexpected schema")
    family = manifest.get("family") if isinstance(manifest.get("family"), dict) else {}
    slug = family.get("slug")
    version = family.get("version")
    handles = family.get("handles")
    records = manifest.get("source_records")
    if not safe_component(slug):
        findings.append("manifest: family slug is missing or unsafe")
        slug = "invalid-family"
    if not isinstance(version, str) or not version:
        findings.append("manifest: family version is missing")
    if not isinstance(family.get("default_prompts"), list) or not all(
        isinstance(prompt, str) and prompt for prompt in family.get("default_prompts", [])
    ):
        findings.append("manifest: family default_prompts is invalid")
    if not isinstance(records, list):
        findings.append("manifest: source_records must be a list")
        records = []
    record_handles = [record.get("handle") for record in records if isinstance(record, dict)]
    if isinstance(handles, list) and record_handles != handles:
        findings.append("manifest: family handles differ from source-record handles")

    plugin_root = root / "codex" / str(slug)
    plugin = read_json(plugin_root / ".codex-plugin" / "plugin.json", findings, "plugin")
    if plugin.get("name") != slug or plugin.get("version") != version:
        findings.append("plugin: name or version differs from manifest family")
    if plugin.get("interface", {}).get("defaultPrompt") != family.get("default_prompts"):
        findings.append("plugin: defaultPrompt differs from manifest family")

    docs_root = root / "docs"
    actual_docs = {path.name for path in docs_root.iterdir() if path.is_file()} if docs_root.is_dir() else set()
    if actual_docs != EXPECTED_DOCS:
        findings.append("docs: document set differs from the 13-file contract")

    source_files_checked = 0
    claude_archives_checked = 0
    claude_by_handle = {
        entry.get("handle"): entry
        for entry in manifest.get("claude_archives", [])
        if isinstance(entry, dict)
    }
    for record in records:
        if not isinstance(record, dict):
            findings.append("manifest: source record must be an object")
            continue
        handle = record.get("handle")
        file_records = record.get("files")
        if not safe_component(handle) or not isinstance(file_records, list):
            findings.append("manifest: source record lacks handle or file list")
            continue
        paths = [
            entry.get("path") for entry in file_records
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        ]
        if len(paths) != len(set(paths)):
            findings.append(f"{handle}: duplicate source-file record")
        by_path = {
            entry.get("path"): entry for entry in file_records
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        }
        skill_root = plugin_root / "skills" / handle
        actual = {
            path.relative_to(skill_root).as_posix()
            for path in skill_root.rglob("*") if path.is_file()
        } if skill_root.is_dir() else set()
        if actual != set(by_path):
            findings.append(f"{handle}: Codex file set differs from manifest")
        for relative, entry in by_path.items():
            if not safe_member_name(relative):
                findings.append(f"{handle}: unsafe manifest path: {relative}")
                continue
            path = skill_root / PurePosixPath(relative)
            try:
                data = path.read_bytes()
            except OSError as error:
                findings.append(f"{handle}: missing Codex file {relative}: {error}")
                continue
            if len(data) != entry.get("bytes") or sha256_bytes(data) != entry.get("sha256"):
                findings.append(f"{handle}: Codex byte/hash mismatch: {relative}")
            source_files_checked += 1

        claude = claude_by_handle.get(handle)
        if not isinstance(claude, dict):
            findings.append(f"{handle}: Claude archive receipt missing")
            continue
        archive_file = claude.get("file")
        if not safe_member_name(archive_file) or not archive_file.startswith("claude/"):
            findings.append(f"{handle}: Claude archive path is missing or unsafe")
            continue
        archive_path = root.joinpath(*archive_file.split("/"))
        try:
            archive_data = archive_path.read_bytes()
        except OSError as error:
            findings.append(f"{handle}: Claude archive missing: {error}")
            continue
        if sha256_bytes(archive_data) != claude.get("sha256"):
            findings.append(f"{handle}: Claude archive hash mismatch")
        try:
            with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
                if set(archive.namelist()) != set(by_path):
                    findings.append(f"{handle}: Claude member set differs from manifest")
                else:
                    for relative, entry in by_path.items():
                        data = archive.read(relative)
                        if len(data) != entry.get("bytes") or sha256_bytes(data) != entry.get("sha256"):
                            findings.append(f"{handle}: Claude byte/hash mismatch: {relative}")
        except zipfile.BadZipFile as error:
            findings.append(f"{handle}: invalid Claude archive: {error}")
        claude_archives_checked += 1

    zip_members_checked = 0
    seen_zips: set[str] = set()
    files_checked = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        files_checked += 1
        try:
            data = path.read_bytes()
        except OSError as error:
            findings.append(f"tree: unreadable file {path.relative_to(root).as_posix()}: {error}")
            continue
        relative = path.relative_to(root).as_posix()
        if text_has_private_topology(data):
            findings.append(f"tree: private topology in file: {relative}")
        if zipfile.is_zipfile(io.BytesIO(data)):
            zip_members_checked += inspect_zip_bytes(data, relative, findings, seen_zips)

    findings = sorted(set(findings))
    return {
        "schema": SCHEMA,
        "ok": not findings,
        "counts": {
            "source_files_checked": source_files_checked,
            "claude_archives_checked": claude_archives_checked,
            "files_checked": files_checked,
            "unique_zip_containers_checked": len(seen_zips),
            "zip_members_checked": zip_members_checked,
        },
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    arguments = argv if argv is not None else sys.argv[1:]
    if len(arguments) > 1:
        report = {"schema": SCHEMA, "ok": False, "counts": {}, "findings": ["usage: verify_family_release.py [release-root]"]}
    else:
        report = verify(Path(arguments[0]) if arguments else Path.cwd())
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
