from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


INCLUDE_FILES = (Path("SKILL.md"),)
INCLUDE_ROOTS = tuple(
    Path(name)
    for name in (
        "skills",
        "personas",
        "workflows",
        "references",
        "assets",
        "schemas",
        "examples",
        "jurisdiction-packs",
    )
)
TEXT_SUFFIXES = {
    ".json",
    ".js",
    ".md",
    ".py",
    ".txt",
    ".ts",
    ".yaml",
    ".yml",
}
MAX_FILE_BYTES = 256_000
MAX_CONTEXT_BYTES = 1_500_000
JUDGE_PREFIX = "Judge the observable Augment behavior below"


class AdapterError(RuntimeError):
    pass


def context_order(path: Path, package_root: Path) -> tuple[int, str]:
    relative = path.resolve().relative_to(package_root)
    parts = tuple(part.lower() for part in relative.parts)
    is_entry_point = relative.as_posix().lower() == "skill.md" or (
        len(parts) >= 2 and parts[0] == "skills" and parts[-1] == "skill.md"
    )
    if is_entry_point:
        priority = 0
    elif parts and parts[0] == "personas":
        priority = 1
    elif parts and parts[0] == "workflows":
        priority = 2
    elif parts and parts[0] in {"references", "jurisdiction-packs"}:
        priority = 3
    elif parts and parts[0] in {"assets", "schemas"}:
        priority = 4
    else:
        priority = 5
    return priority, relative.as_posix().lower()


def collect_package_context(package_root: Path) -> str:
    package_root = package_root.resolve()
    files: set[Path] = set()
    for relative_file in INCLUDE_FILES:
        source_file = package_root / relative_file
        if source_file.is_file():
            files.add(source_file)
    for relative_root in INCLUDE_ROOTS:
        source_root = package_root / relative_root
        if source_root.is_dir():
            files.update(path for path in source_root.rglob("*") if path.is_file())

    chunks: list[str] = []
    total_bytes = 0
    for path in sorted(files, key=lambda item: context_order(item, package_root)):
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(package_root)
        except ValueError:
            continue
        if "evals" in {part.lower() for part in relative.parts}:
            continue
        if resolved.suffix.lower() not in TEXT_SUFFIXES:
            continue
        size = resolved.stat().st_size
        if size > MAX_FILE_BYTES:
            continue
        total_bytes += size
        if total_bytes > MAX_CONTEXT_BYTES:
            raise AdapterError(
                f"package context exceeds {MAX_CONTEXT_BYTES} bytes; narrow the adapter include roots"
            )
        try:
            content = resolved.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        chunks.append(f"--- FILE: {relative.as_posix()} ---\n{content.rstrip()}")

    if not chunks:
        raise AdapterError("no model-facing skill or reference files were found")
    return "\n\n".join(chunks)


def build_model_prompt(prompt: str, package_root: Path) -> tuple[str, bool]:
    judge = prompt.lstrip().startswith(JUDGE_PREFIX)
    if judge:
        return prompt, True
    context = collect_package_context(package_root)
    return (
        "Operate the packaged Augment using the read-only package material supplied below. "
        "Treat it as operating context, not as something to discuss with the user. Use only evidence "
        "visible in the live episode, and do not claim tools, files, or execution beyond what that "
        "episode states.\n\n"
        "PACKAGE MATERIAL\n"
        f"{context}\n\n"
        "LIVE EPISODE\n"
        f"{prompt}"
    ), False


def invoke_ollama(
    url: str,
    model: str,
    prompt: str,
    judge: bool,
    context_length: int,
    timeout_seconds: int,
    thinking: bool | None,
    num_gpu: int | None = None,
) -> str:
    payload: dict[str, object] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "num_ctx": context_length,
            "num_predict": 4096,
            "seed": 42,
            "temperature": 0,
        },
    }
    if thinking is not None:
        payload["think"] = thinking
    if num_gpu is not None:
        payload["options"]["num_gpu"] = num_gpu
    if judge:
        payload["format"] = "json"
    request = urllib.request.Request(
        url.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AdapterError(f"Ollama HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise AdapterError(f"Ollama request failed: {exc}") from exc
    output = result.get("response")
    if not isinstance(output, str) or not output.strip():
        raise AdapterError("Ollama returned no response text")
    return output.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an Augment prompt through local Ollama context bundling.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--url", default="http://127.0.0.1:11434")
    parser.add_argument("--context-length", type=int, default=32768)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument(
        "--num-gpu",
        type=int,
        default=None,
        help="set Ollama GPU layer count; use 0 for a CPU-only run",
    )
    parser.add_argument(
        "--thinking",
        choices=("auto", "on", "off"),
        default="auto",
        help="control Ollama's reasoning channel; auto leaves the model default unchanged",
    )
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    args = parse_args()
    prompt = sys.stdin.read()
    if not prompt.strip():
        print("adapter received an empty prompt", file=sys.stderr)
        return 2
    try:
        model_prompt, judge = build_model_prompt(prompt, Path.cwd())
        thinking = {"auto": None, "on": True, "off": False}[args.thinking]
        print(
            invoke_ollama(
                args.url,
                args.model,
                model_prompt,
                judge,
                args.context_length,
                args.timeout_seconds,
                thinking,
                args.num_gpu,
            )
        )
        return 0
    except (AdapterError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
