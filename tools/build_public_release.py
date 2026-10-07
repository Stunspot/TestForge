#!/usr/bin/env python3
"""Build the deterministic current TestForge dual-host customer release."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
import os
import tempfile
from archive_paths import check_tree, assert_unlinked
from source_text_policy import assert_text_entries, assert_source_text
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.0.0"
DATE = "2026-09-05"
OUT = ROOT / "releases" / f"v{VERSION}"
PREFIX = f"testforge-v{VERSION}"
HANDLES = ("software-verification", "verification-reviewer")
DOCS = (
    "README.md", "QUICK-START.md", "INSTALL-CODEX.md", "INSTALL-CLAUDE.md",
    "CAPABILITIES.md", "LIMITATIONS.md", "SUPPORT.md", "VALIDATION.md",
    "MAINTAINER-GUIDE.md", "PACKAGE-REFERENCE.md", "DESCRIPTION-CUSTODY.md",
    "PROVENANCE.md", "HOST-EVIDENCE-BOUNDARY.md",
)
ZIP_TIME = (2026, 9, 5, 12, 0, 0)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def files(root: Path):
    assert_unlinked(root)
    return sorted((p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts), key=lambda p: p.relative_to(root).as_posix())


def zip_tree(source: Path, target: Path, prefix: str = "") -> None:
    paths = [p for p in files(source) if p.resolve() != target.resolve()]
    entries = check_tree(source, paths, prefix)
    assert_text_entries(entries)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_path = tempfile.mkstemp(prefix=".testforge-", suffix=".building", dir=target.parent)
    os.close(fd)
    temporary = Path(temporary_path)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, payload in entries:
                info = zipfile.ZipInfo(name, ZIP_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, payload)
        os.replace(temporary, target)
    finally:
        if temporary.exists(): temporary.unlink()


def source_record(handle: str, root: Path) -> dict:
    inventory = []
    for path in files(root):
        data = path.read_bytes()
        inventory.append({"bytes": len(data), "path": path.relative_to(root).as_posix(), "sha256": digest(data)})
    return {"files": inventory, "handle": handle}


def require_final_seal(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--final-seal",
        action="store_true",
        help="confirm implementation, tests, documentation, and independent review are complete",
    )
    parser.add_argument("--output-dir", type=Path, help="new directory directly under releases; an accepted output is never overwritten")
    args = parser.parse_args(argv)
    if not args.final_seal:
        parser.error("release hashing is final-only; finish and review the candidate, then pass --final-seal")
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if status.returncode != 0:
        parser.error("cannot establish a clean frozen repository for final sealing")
    if status.stdout.strip():
        parser.error("final sealing requires a clean frozen repository; commit or otherwise resolve all changes first")
    return args


def main(argv: list[str] | None = None) -> int:
    args = require_final_seal(argv)
    out = args.output_dir or OUT
    if out.parent.resolve() != (ROOT / "releases").resolve():
        raise RuntimeError("unsafe release target")
    if out.exists():
        raise RuntimeError("release output already exists; choose a new --output-dir and preserve accepted bytes")
    assert_unlinked(ROOT / "plugins" / "testforge")
    assert_unlinked(ROOT / "release-docs")
    # Check the exact working inputs before creating any public output.
    assert_source_text(files(ROOT / "plugins" / "testforge") + files(ROOT / "release-docs") + [ROOT / "LICENSE.md", ROOT / "tools" / "verify_family_release.py"])
    (out / "codex").mkdir(parents=True)
    (out / "claude").mkdir()
    (out / "docs").mkdir()
    (out / "tools").mkdir()
    shutil.copy2(ROOT / "LICENSE.md", out / "LICENSE.md")
    shutil.copytree(ROOT / "plugins" / "testforge", out / "codex" / "testforge", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.pyo"))
    shutil.copy2(ROOT / "tools" / "verify_family_release.py", out / "tools" / "verify_release.py")
    for name in DOCS:
        text = (ROOT / "release-docs" / name).read_text(encoding="utf-8")
        text = text.replace(f"../releases/v{VERSION}/", "../")
        (out / "docs" / name).write_text(text, encoding="utf-8", newline="\n")
    manifest = {
        "claude_archives": [],
        "excluded_generated_caches": {handle: [] for handle in HANDLES},
        "excluded_local_configuration": {handle: [] for handle in HANDLES},
        "family": {
            "backup_filename": f"TestForge-v{VERSION}.zip",
            "default_prompts": json.loads((out / "codex" / "testforge" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))["interface"]["defaultPrompt"],
            "handles": list(HANDLES), "primary_handle_custody": True,
            "repository": "Stunspot/TestForge", "repository_state": "existing",
            "short_description": "Test uncertainty into release proof and challenge.",
            "slug": "testforge",
            "summary": "Risk-based software verification, evidence-backed release judgment, and adversarial review of verification claims.",
            "title": "TestForge", "version": VERSION, "visibility": "PUBLIC",
        },
        "package_claim_boundary": "Static package and byte-parity evidence only; no host activation, live behavior, or publication claim.",
        "schema": "cd-settled-family-release/v1",
        "source_records": [],
    }
    for handle in HANDLES:
        source = out / "codex" / "testforge" / "skills" / handle
        manifest["source_records"].append(source_record(handle, source))
        archive = out / "claude" / f"{handle}-v{VERSION}.zip"
        zip_tree(source, archive)
        manifest["claude_archives"].append({"file": f"claude/{archive.name}", "handle": handle, "sha256": digest(archive.read_bytes())})
    write_json(out / "manifest.json", manifest)

    package_receipt = {
        "schema": "cd-family-package-receipt/v1", "family": "testforge", "version": VERSION,
        "built_at": f"{DATE}T12:00:00-05:00", "status": "static-package-built",
        "claim_boundary": manifest["package_claim_boundary"],
        "codex_plugin": "codex/testforge", "claude_archives": manifest["claude_archives"],
    }
    write_json(out / "package-receipt.json", package_receipt)
    write_json(out / "description-custody.json", {
        "schema": "cd-description-custody/v1", "family": "TestForge", "version": VERSION,
        "short_description": manifest["family"]["short_description"], "summary": manifest["family"]["summary"],
    })
    write_json(out / "receipt.json", {
        "schema": "cd-release-receipt/v1", "family": "TestForge", "version": VERSION,
        "release_date": DATE, "artifact": f"TestForge-v{VERSION}.zip",
        "claim_boundary": manifest["package_claim_boundary"],
    })

    report = subprocess.run([sys.executable, "-B", str(out / "tools" / "verify_release.py"), str(out)], check=True, capture_output=True, text=True)
    write_json(out / "verification-report.json", json.loads(report.stdout))
    outer = out / f"TestForge-v{VERSION}.zip"
    zip_tree(out, outer, PREFIX)
    outer_hash = digest(outer.read_bytes())
    (out / f"TestForge-v{VERSION}.zip.sha256").write_text(f"{outer_hash}  {outer.name}\n", encoding="ascii", newline="\n")
    print(json.dumps({"artifact": str(outer), "sha256": outer_hash, "version": VERSION}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
