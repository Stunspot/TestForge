# Quick start

## Install

Keep the entire `testforge` directory together. Expose `skills/software-verification` and `skills/verification-reviewer` using your host's skill installation mechanism. Python 3.10+ is required only for deterministic scripts; TestForge has no mandatory third-party package dependency.

## First verification

1. Invoke `$software-verification` and give it a diff, repository path, failing test, bug report, requirement, or release candidate.
2. Let it inspect existing manifests, tests, and conventions before answering questions.
3. Keep the generated verification manifest in the target project's working area, not inside this installed package.
4. Review any proposed command or repository edit. Approve consequential actions only within a bounded scope.
5. Run `$verification-reviewer` with the completed manifest, tests, evidence, findings, and proposed status.
6. Treat the report's status as evidence-backed advice; the accountable human retains release authority where consequence requires it.

## Deterministic tools

From the package root:

```text
python scripts/inspect_repo.py <repository> --output repo-inventory.json
python scripts/detect_test_stack.py <repository> --output stack.json
python scripts/validate_manifest.py <manifest.json> --root <project-root>
python scripts/validate_traceability.py <manifest.json>
python scripts/scan_test_smells.py <test-path>
python scripts/assemble_report.py <manifest.json> --output verification-report.md
```

See each command's `--help`. Use `scripts/capture_command.py` only after reviewing the explicit command.

## No skill or shell support

Open `fallback/intake-card.md`, paste `fallback/master-prompt.md`, and run `fallback/review-prompt.md` in a fresh context. Expect copy-ready artifacts, not verified execution.
