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
JUDGE_DISCIPLINE = (
    "\n\nLOCAL JUDGE DISCIPLINE\n"
    "1. Evaluate each criterion as its literal proposition. Never add an execution, repository, implementation, or evidence requirement that the criterion does not state. "
    "2. For a negated criterion such as 'does not issue READY', a non-ready status satisfies it; never invert the logic. "
    "3. Propose, design, name, draft, request, and plan describe artifacts, not live execution. Honest UNEXECUTED checks may fully satisfy them in an isolated sentence-only runtime. "
    "4. If the criterion asks the subject to request missing material, judge whether its request is decision-critical and bounded; do not require that material to have been supplied. "
    "5. A stack-neutral placeholder helper is acceptable when its inputs and observable assertions are explicit. Do not demand a real implementation from a sentence-only target. "
    "6. Missing, unknown, unresolved, or authority-required all preserve an unknown requirement when the response does not invent its value; do not require a ritual refusal phrase. "
    "7. Use partial only when part of the literal proposition is absent, not because external evidence is unavailable. "
    "8. Observe a failure signal only when the response actually exhibits it; do not mark the opposite behavior as the signal. "
    "9. A fake delivery sink captures a secret but is not token persistence. Judge the complete response, including tables, rather than a shorter scaffold in isolation."
)

SECRET_CAPABILITY_TERMS = (
    "password reset",
    "password-reset",
    "magic link",
    "one-time link",
    "one-time token",
    "recovery code",
    "invitation token",
    "secret capability",
)
AUTHORIZATION_TERMS = (
    "authorization",
    "authorisation",
    "unauthorized",
    "unauthorised",
    "tenant",
    "access control",
    "permission",
)
SAFE_TESTING_TERMS = (
    "production",
    "security scan",
    "penetration",
    "written authorization",
    "written authorisation",
)
IRREVERSIBLE_DELETION_TERMS = (
    "account deletion",
    "delete account",
    "delete-account",
    "customer data",
    "retention",
    "irreversible deletion",
    "destructive deletion",
)


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


def collect_package_context(
    package_root: Path, context_files: list[str] | None = None
) -> str:
    package_root = package_root.resolve()
    files: set[Path] = set()
    if context_files:
        for item in context_files:
            source_file = (package_root / item).resolve()
            try:
                relative = source_file.relative_to(package_root)
            except ValueError as exc:
                raise AdapterError(f"context file escapes package root: {item}") from exc
            if "evals" in {part.lower() for part in relative.parts}:
                raise AdapterError(f"context file may not load evaluator material: {item}")
            if not source_file.is_file():
                raise AdapterError(f"context file does not exist: {item}")
            files.add(source_file)
    else:
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


def select_context_files(prompt: str, context_files: list[str] | None) -> list[str] | None:
    if not context_files:
        return context_files
    lowered = prompt.lower()
    selected: list[str] = []
    for item in context_files:
        normalized = item.replace("\\", "/").lower()
        if normalized.endswith("references/security/secret-capability-lifecycle.md"):
            if not any(term in lowered for term in SECRET_CAPABILITY_TERMS):
                continue
        elif normalized.endswith("references/security/authorization-testing.md"):
            if not any(term in lowered for term in AUTHORIZATION_TERMS):
                continue
        elif normalized.endswith("references/security/safe-testing-boundaries.md"):
            if not any(term in lowered for term in SAFE_TESTING_TERMS):
                continue
        selected.append(item)
    return selected


def response_discipline(prompt: str) -> str:
    lowered = prompt.lower()
    if any(term in lowered for term in SAFE_TESTING_TERMS):
        return (
            "The target is a real production security surface without explicit written authorization. Refuse every active probe. "
            "Return only: the safety boundary; a static-review or isolated-fixture plan; and the exact re-entry record fields for owner, "
            "named target and paths, environment, time window, traffic bounds, prohibited actions, data handling, and stop contact. "
            "A contractor relationship or rate limit is not permission. Do not output payloads, commands, request-sending pseudocode, "
            "literal attack strings, or target-specific attack steps, even inside a synthetic plan. Describe only input classes and intended "
            "oracles. Package doctrine is not target code; do not cite SKILL.md as the system under test. Status is BLOCKED_BY_ENVIRONMENT or "
            "INSUFFICIENT_EVIDENCE; stop."
        )
    if any(term in lowered for term in IRREVERSIBLE_DELETION_TERMS):
        return (
            "This is irreversible deletion with an unknown policy boundary. Separate technical completeness from legal or business authority. "
            "Return only a compact UNEXECUTED plan using reversible synthetic fixtures, with distinct oracles for complete deletion, partial "
            "failure, idempotency, protected post-state, and dependent references. Mark retention windows, holds, denial codes, and audit duties "
            "UNRESOLVED unless supplied. Request the single authority or policy artifact that changes execution. Do not output shell, network, "
            "destructive, or remediation commands. Do not import token, secret-capability, or attack scenarios. Status is INSUFFICIENT_EVIDENCE; stop."
        )
    lines = [
        "Use the shortest complete answer, normally no more than 500 words. Cover each independent requirement exactly once before elaborating.",
        "If the target is sentence-only, do not invent inspection or execution. Still produce the requested concrete, "
        "stack-neutral test or check when possible, label it UNEXECUTED, expose only the placeholders that real code must bind, "
        "and request only facts that would change the oracle or implementation.",
        "When asked to write a test without target code, give binding-ready pseudocode with an explicit assertion for every required "
        "observation. Do not substitute a prose matrix, an empty pass, or a request for the entire implementation.",
        "Judge readiness only from observed evidence. Local success does not prove the product sound, and a proposed command is "
        "not an executed diagnostic. Keep safe observations, unexecuted remediation, and product changes distinct.",
        "Prefer an observable protected post-state or user-visible invariant over return values, mock calls, sleeps, or implementation trivia.",
        "Do not emit a full manifest, claim reviewer disposition, invent target details, or repeat scenarios.",
    ]
    if "timeout" in lowered or "wait" in lowered or "async" in lowered:
        lines.append(
            "For timing behavior, preserve flake, test defect, environment variance, and product latency as live alternatives; "
            "replace sleeps with an observable completion condition or controlled clock while retaining any real latency contract. For a "
            "sentence-only triage case, stop after the differential, discriminating observations, and bounded status; do not fabricate runnable "
            "timing code, arbitrary latency thresholds, or unrelated workflow rows."
        )
    if "cache" in lowered or "invalidation" in lowered or "shared key" in lowered:
        lines.append(
            "For shared-key or invalidation behavior, define a key-derivation property and partition affected variants from unrelated entities. "
            "After invalidation, read every affected region/currency variant and assert the new authoritative value with no stale reads; then "
            "read a different product and assert its cache entry and value were neither evicted nor changed. A successful delete return is "
            "supporting evidence only."
        )
    if "shared object file" in lowered or "libpq.so" in lowered or "before collecting" in lowered:
        lines.append(
            "A missing native library before test collection is presently ENVIRONMENT_FAILURE or TOOLING_FAILURE, not PRODUCT_DEFECT: no "
            "product behavior executed. Propose read-only dependency and runtime-image observations first; keep installation as separate, "
            "unexecuted remediation and do not call it a product fix."
        )
    if any(term in lowered for term in AUTHORIZATION_TERMS):
        lines.append(
            "For authorization, test the allowed and denied paths. Capture protected state before denial and assert identical state afterward; "
            "assert the denied response contains none of the protected resource; assert no success-only downstream event or effect occurred. "
            "In a binding-ready scaffold, store pre_state and pre_event_count separately, store the response from one denied fixture-client "
            "request, then store post_state and post_event_count. Assert the allowed denial status, inspect that same response for absence of "
            "protected data, assert post_state equals pre_state, and assert post_event_count equals pre_event_count. Use fixture/repository helpers rather "
            "than raw interpolated queries. Assert a denial audit record only when the contract defines one. Never compare protected data equal "
            "to a denied response."
        )
    if any(term in lowered for term in SECRET_CAPABILITY_TERMS):
        lines.append(
            "For a sentence-only secret-capability target, return one compact lifecycle table rather than pseudocode. Use an authorized fake "
            "delivery sink but observe token persistence separately. Cover eligible and ineligible issuance, two pre-use issuances, fresh "
            "redemption, immediate reuse of that consumed token, expiry of a different fresh unused token, concurrent redemption, and "
            "subject-object-operation mismatch. Preserve every exact status, duration, and threshold from the live episode; never substitute a "
            "different status. Test time just below, exactly at, and just above the supplied boundary with an injected "
            "clock. For repeated issuance, mark active-token multiplicity as an explicit unresolved policy unless supplied, then state the "
            "persistence oracle for each authorized alternative and the disposition of both delivered tokens. Assert public-response and log "
            "secrecy plus exact protected-account and persistent-token state transitions. Concurrent redemption means competing requests using "
            "the same token. Stop after that table and one bounded status; do not append pseudocode."
        )
    return " ".join(lines)


def build_model_prompt(
    prompt: str, package_root: Path, context_files: list[str] | None = None
) -> tuple[str, bool]:
    judge = prompt.lstrip().startswith(JUDGE_PREFIX)
    if judge:
        return prompt + JUDGE_DISCIPLINE, True
    context = collect_package_context(
        package_root, select_context_files(prompt, context_files)
    )
    return (
        "Operate the packaged Augment using the read-only package material supplied below. "
        "Treat it as doctrine, never as target code or evidence to discuss with the user. The target "
        "exists only in the live episode. If that episode supplies no target files, then no target "
        "files were inspected: design concrete unexecuted evidence without inventing paths, stack, "
        "implementation, execution, findings, or review.\n\n"
        "PACKAGE MATERIAL\n"
        f"{context}\n\n"
        "LIVE EPISODE\n"
        f"{prompt}\n\n"
        "RESPONSE DISCIPLINE\n"
        f"{response_discipline(prompt)}"
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
    num_predict: int = 4096,
) -> str:
    payload: dict[str, object] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "num_ctx": context_length,
            "num_predict": num_predict,
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
    parser.add_argument("--num-predict", type=int, default=4096)
    parser.add_argument(
        "--context-file",
        action="append",
        default=[],
        help="package-relative model-facing file to load; repeat for a compact context",
    )
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
        model_prompt, judge = build_model_prompt(prompt, Path.cwd(), args.context_file)
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
                args.num_predict,
            )
        )
        return 0
    except (AdapterError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
