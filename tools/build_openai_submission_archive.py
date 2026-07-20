#!/usr/bin/env python3
"""Build a deterministic OpenAI skills-only submission ZIP from a Codex plugin."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import struct
import zipfile


FIXED_TIME = (2026, 1, 1, 0, 0, 0)
EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache"}
MANIFEST_PATH = PurePosixPath(".codex-plugin/plugin.json")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_archive_bytes(path: Path) -> tuple[bytes, bool]:
    """Return cross-platform bytes while preserving non-UTF-8 and binary files."""
    data = path.read_bytes()
    if b"\x00" in data:
        return data, False
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data, False
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return canonical, canonical != data


def regular_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not EXCLUDED_PARTS.intersection(path.relative_to(root).parts)
    )


def resolve_asset(root: Path, value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.startswith("./"):
        raise ValueError(f"interface.{field} must be a ./-relative path")
    target = (root / value.removeprefix("./")).resolve()
    if root.resolve() not in target.parents:
        raise ValueError(f"interface.{field} escapes the plugin root")
    if not target.is_file():
        raise ValueError(f"interface.{field} does not exist: {value}")
    return target


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def submission_manifest(plugin_root: Path) -> tuple[dict[str, object], dict[str, object]]:
    manifest_path = plugin_root / MANIFEST_PATH
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if not isinstance(manifest, dict):
        raise ValueError("plugin manifest must be an object")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise ValueError("plugin interface must be an object")
    for field, minimum in (("composerIcon", 48), ("logo", 256)):
        asset = resolve_asset(plugin_root, interface.get(field), field)
        width, height = png_dimensions(asset)
        if width != height or width < minimum:
            raise ValueError(
                f"interface.{field} must be a square PNG at least {minimum}x{minimum}; "
                f"found {width}x{height}"
            )

    transformed = dict(manifest)
    transformed["interface"] = {
        "composerIcon": interface["composerIcon"],
        "logo": interface["logo"],
    }
    metadata = {
        "kept_interface_fields": ["composerIcon", "logo"],
        "omitted_interface_fields": sorted(set(interface) - {"composerIcon", "logo"}),
    }
    return transformed, metadata


def build(plugin_root: Path, output: Path, top_level: str) -> dict[str, object]:
    plugin_root = plugin_root.resolve()
    if not plugin_root.is_dir():
        raise ValueError(f"plugin root does not exist: {plugin_root}")
    manifest, transform = submission_manifest(plugin_root)
    rendered_manifest = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    source_manifest, _ = canonical_archive_bytes(plugin_root / MANIFEST_PATH)
    files = regular_files(plugin_root)
    normalized_text_members: list[str] = []
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_STORED,
    ) as archive:
        for path in files:
            relative = PurePosixPath(path.relative_to(plugin_root).as_posix())
            name = PurePosixPath(top_level, relative).as_posix()
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            if relative == MANIFEST_PATH:
                data = rendered_manifest
            else:
                data, normalized = canonical_archive_bytes(path)
                if normalized:
                    normalized_text_members.append(relative.as_posix())
            archive.writestr(info, data)

    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if any("\\" in name for name in names):
            raise RuntimeError("submission archive contains a backslash path")
        archived_manifest = archive.read(f"{top_level}/{MANIFEST_PATH.as_posix()}")
        observed = json.loads(archived_manifest.decode("utf-8"))
        if observed.get("interface") != manifest["interface"]:
            raise RuntimeError("submission manifest round trip failed")

    return {
        "schema_version": "cd-openai-plugin-submission-custody/v1",
        "plugin": {"name": manifest.get("name", ""), "version": manifest.get("version", "")},
        "source_plugin_root": plugin_root.name,
        "top_level": top_level,
        "archive_name": output.name,
        "archive_sha256": sha256_file(output),
        "bytes": output.stat().st_size,
        "member_count": len(files),
        "source_manifest_sha256": sha256_bytes(source_manifest),
        "submission_manifest_sha256": sha256_bytes(rendered_manifest),
        "text_canonicalization": "UTF-8 text is stored as LF without a BOM; binary and non-UTF-8 bytes are preserved",
        "normalized_text_member_count": len(normalized_text_members),
        "zip_compression": "stored",
        "manifest_transform": transform,
        "archive_paths_use_forward_slashes": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--top-level")
    args = parser.parse_args()

    manifest = json.loads(
        (args.plugin_root / MANIFEST_PATH).read_text(encoding="utf-8-sig")
    )
    top_level = args.top_level or f"{manifest.get('name', args.plugin_root.name)}-plugin"
    report = build(args.plugin_root, args.output, top_level)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
