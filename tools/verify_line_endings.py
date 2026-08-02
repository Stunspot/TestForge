#!/usr/bin/env python3
"""Verify the Collaborative Dynamics line-ending contract in a Git index."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "testforge-line-ending-policy/v1"
ROOT_BYTE_CUSTODY = re.compile(r"^\*\s+-text(?:\s*(?:#.*)?)?$", re.MULTILINE)
BINARY_PROBES = ("zip", "docx", "xlsx", "pptx", "pdf", "png", "jpg", "jpeg", "gif", "ico")


class VerificationError(RuntimeError):
    """Raised when the verifier cannot inspect the requested repository."""


def run_git(root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(
        ["git", "-c", "core.autocrlf=false", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        env=environment,
    )


def git_output(root: Path, *arguments: str) -> str:
    completed = run_git(root, *arguments)
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).decode("utf-8", errors="replace").strip()
        raise VerificationError(f"git {' '.join(arguments)} failed: {detail}")
    return completed.stdout.decode("utf-8", errors="replace")


def finding(code: str, message: str, path: str | None = None) -> dict[str, str]:
    result = {"code": code, "message": message}
    if path is not None:
        result["path"] = path
    return result


def verify_lf_policy_file(path: Path, findings: list[dict[str, str]]) -> None:
    data = path.read_bytes()
    if b"\r" in data:
        findings.append(finding("POLICY_FILE_CR", "Policy file contains CR bytes.", path.name))
    if not data.endswith(b"\n"):
        findings.append(finding("POLICY_FILE_FINAL_LF", "Policy file lacks a final LF.", path.name))


def resolved_attributes(root: Path, probe: str) -> dict[str, str]:
    output = git_output(root, "check-attr", "text", "eol", "binary", "--", probe)
    result: dict[str, str] = {}
    prefix = f"{probe}: "
    for line in output.splitlines():
        if not line.startswith(prefix):
            continue
        attribute, separator, value = line[len(prefix) :].partition(": ")
        if separator:
            result[attribute] = value
    return result


def editorconfig_values(data: bytes) -> dict[tuple[str | None, str], str]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise VerificationError(".editorconfig is not UTF-8") from error
    section: str | None = None
    values: dict[tuple[str | None, str], str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line.casefold()
            continue
        key, separator, value = line.partition("=")
        if separator:
            values[(section, key.strip().casefold())] = value.strip().casefold()
    return values


def editorconfig_windows_crlf(values: dict[tuple[str | None, str], str], extension: str) -> bool:
    combined = values.get(("[*.{bat,cmd}]", "end_of_line"))
    specific = values.get((f"[*.{extension}]", "end_of_line"))
    return combined == "crlf" or specific == "crlf"


def verify_editorconfig(path: Path, findings: list[dict[str, str]]) -> None:
    verify_lf_policy_file(path, findings)
    try:
        values = editorconfig_values(path.read_bytes())
    except VerificationError as error:
        findings.append(finding("EDITORCONFIG_ENCODING", str(error), path.name))
        return
    required = {
        (None, "root"): "true",
        ("[*]", "charset"): "utf-8",
        ("[*]", "end_of_line"): "lf",
        ("[*]", "insert_final_newline"): "true",
    }
    for key, expected in required.items():
        if values.get(key) != expected:
            findings.append(
                finding(
                    "EDITORCONFIG_BASELINE",
                    f"Expected {key[1]}={expected} in {key[0] or 'root'}, found {values.get(key)!r}.",
                    path.name,
                )
            )
    for extension in ("bat", "cmd"):
        if not editorconfig_windows_crlf(values, extension):
            findings.append(
                finding(
                    "EDITORCONFIG_WINDOWS_CRLF",
                    f"No CRLF EditorConfig override applies to *.{extension}.",
                    path.name,
                )
            )


def cached_text_attributes(root: Path, paths: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for offset in range(0, len(paths), 100):
        chunk = paths[offset : offset + 100]
        completed = run_git(root, "check-attr", "--cached", "-z", "text", "--", *chunk)
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).decode("utf-8", errors="replace").strip()
            raise VerificationError(f"git check-attr --cached failed: {detail}")
        fields = [field.decode("utf-8", errors="replace") for field in completed.stdout.split(b"\0") if field]
        if len(fields) % 3:
            raise VerificationError("git check-attr --cached returned malformed output")
        for index in range(0, len(fields), 3):
            path, attribute, value = fields[index : index + 3]
            if attribute == "text":
                values[path] = value
    return values


def indexed_blobs(root: Path) -> list[tuple[str, str]]:
    completed = run_git(root, "ls-files", "--stage", "-z")
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).decode("utf-8", errors="replace").strip()
        raise VerificationError(f"git ls-files --stage failed: {detail}")
    blobs: list[tuple[str, str]] = []
    for record in completed.stdout.split(b"\0"):
        if not record:
            continue
        metadata, separator, path_bytes = record.partition(b"\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            raise VerificationError("git ls-files --stage returned malformed output")
        mode, object_id, stage = fields
        if stage != b"0":
            continue
        if mode == b"160000":
            continue
        if mode not in {b"100644", b"100755", b"120000"}:
            raise VerificationError(
                f"git ls-files --stage returned unsupported mode {mode.decode('ascii', errors='replace')}"
            )
        blobs.append(
            (
                path_bytes.decode("utf-8", errors="replace"),
                object_id.decode("ascii"),
            )
        )
    return blobs


def blob_cr_paths(root: Path, blobs: list[tuple[str, str]]) -> list[str]:
    if not blobs:
        return []
    process = subprocess.Popen(
        ["git", "-c", "core.autocrlf=false", "cat-file", "--batch"],
        cwd=root,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    request = "".join(f"{object_id}\n" for _path, object_id in blobs).encode("ascii")
    stdout, stderr = process.communicate(request)
    if process.returncode != 0:
        detail = (stderr or stdout).decode("utf-8", errors="replace").strip()
        raise VerificationError(f"git cat-file --batch failed: {detail}")

    offset = 0
    paths: list[str] = []
    for path, expected_id in blobs:
        header_end = stdout.find(b"\n", offset)
        if header_end < 0:
            raise VerificationError("git cat-file --batch returned a truncated header")
        header = stdout[offset:header_end].split()
        if len(header) != 3:
            raise VerificationError("git cat-file --batch returned malformed object metadata")
        object_id, object_type, size_bytes = header
        if object_id.decode("ascii") != expected_id or object_type != b"blob":
            raise VerificationError("git cat-file --batch returned an unexpected object")
        try:
            size = int(size_bytes)
        except ValueError as error:
            raise VerificationError("git cat-file --batch returned an invalid blob size") from error
        content_start = header_end + 1
        content_end = content_start + size
        if content_end >= len(stdout) or stdout[content_end : content_end + 1] != b"\n":
            raise VerificationError("git cat-file --batch returned truncated blob content")
        if b"\r" in stdout[content_start:content_end]:
            paths.append(path)
        offset = content_end + 1
    if offset != len(stdout):
        raise VerificationError("git cat-file --batch returned unexpected trailing output")
    return paths


def indexed_text_with_cr(root: Path) -> list[str]:
    blobs = indexed_blobs(root)
    attributes = cached_text_attributes(root, [path for path, _object_id in blobs])
    text_blobs = [
        (path, object_id)
        for path, object_id in blobs
        if attributes.get(path) != "unset"
    ]
    return sorted(blob_cr_paths(root, text_blobs))


def verify(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if run_git(root, "rev-parse", "--is-inside-work-tree").returncode != 0:
        raise VerificationError(f"not a Git worktree: {root}")

    findings: list[dict[str, str]] = []
    attributes_path = root / ".gitattributes"
    if not attributes_path.is_file():
        return {
            "schema": SCHEMA,
            "status": "FAIL",
            "profile": "missing",
            "root": str(root),
            "findings": [finding("GITATTRIBUTES_MISSING", "Repository lacks .gitattributes.", ".gitattributes")],
            "probes": {},
            "indexed_text_cr_paths": [],
        }

    try:
        attributes_text = attributes_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        attributes_text = ""
        findings.append(finding("GITATTRIBUTES_ENCODING", ".gitattributes is not UTF-8.", ".gitattributes"))

    profile = "byte-custody" if ROOT_BYTE_CUSTODY.search(attributes_text) else "standard"
    probes: dict[str, dict[str, str]] = {}
    if profile == "byte-custody":
        probe = ".testforge-line-ending-probe.txt"
        probes[probe] = resolved_attributes(root, probe)
        if probes[probe].get("text") != "unset":
            findings.append(
                finding("BYTE_CUSTODY_INEFFECTIVE", f"Root byte custody did not resolve text=unset: {probes[probe]}")
            )
        cr_paths: list[str] = []
    else:
        verify_lf_policy_file(attributes_path, findings)
        editorconfig_path = root / ".editorconfig"
        if editorconfig_path.is_file():
            verify_editorconfig(editorconfig_path, findings)
        else:
            findings.append(finding("EDITORCONFIG_MISSING", "Repository lacks .editorconfig.", ".editorconfig"))

        expected_probes: dict[str, dict[str, set[str]]] = {
            ".testforge-line-ending-probe.txt": {"text": {"auto", "set"}, "eol": {"lf"}},
            ".testforge-line-ending-probe.bat": {"text": {"set"}, "eol": {"crlf"}},
            ".testforge-line-ending-probe.cmd": {"text": {"set"}, "eol": {"crlf"}},
        }
        for extension in BINARY_PROBES:
            expected_probes[f".testforge-line-ending-probe.{extension}"] = {"text": {"unset"}}

        for probe, expected in expected_probes.items():
            resolved = resolved_attributes(root, probe)
            probes[probe] = resolved
            for attribute, allowed in expected.items():
                if resolved.get(attribute) not in allowed:
                    findings.append(
                        finding(
                            "ATTRIBUTE_MISMATCH",
                            f"{probe} expected {attribute} in {sorted(allowed)}, resolved {resolved}.",
                            ".gitattributes",
                        )
                    )

        cr_paths = indexed_text_with_cr(root)
        for path in cr_paths:
            findings.append(
                finding(
                    "INDEXED_TEXT_CR",
                    "Tracked non-binary blob contains CR bytes; normalize it to LF in the Git index.",
                    path,
                )
            )

    return {
        "schema": SCHEMA,
        "status": "PASS" if not findings else "FAIL",
        "profile": profile,
        "root": str(root),
        "findings": findings,
        "probes": probes,
        "indexed_text_cr_paths": cr_paths,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json-out", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = verify(args.root)
    except (OSError, VerificationError) as error:
        report = {
            "schema": SCHEMA,
            "status": "ERROR",
            "profile": "unknown",
            "root": str(args.root.resolve()),
            "findings": [finding("VERIFIER_ERROR", str(error))],
            "probes": {},
            "indexed_text_cr_paths": [],
        }
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered, encoding="utf-8", newline="\n")
    sys.stdout.write(rendered)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
