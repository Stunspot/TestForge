# Quick start

## Install

Each v1.1.1 skill is self-contained. Python 3.10+ is required only for deterministic scripts; TestForge has no mandatory third-party package dependency.

Use [Install in Codex](INSTALL-CODEX.md) or [Install in Claude](INSTALL-CLAUDE.md). Install and verify both skills separately. Structural validation proves the package shape; successful discovery requires a fresh host task or conversation.

### Claude Code

Copy both complete skill directories into `~/.claude/skills/` for personal use or `.claude/skills/` for one project. Invoke `/software-verification` and `/verification-reviewer` when explicit selection is useful.

## First verification

1. Invoke `$software-verification` and give it a diff, repository path, failing test, bug report, requirement, or release candidate.
2. Let it inspect existing manifests, tests, and conventions before answering questions.
3. Keep the generated verification manifest in the target project's working area, not inside this installed package.
4. Review any proposed command or repository edit. Approve consequential actions only within a bounded scope.
5. Run `$verification-reviewer` with the completed manifest, tests, evidence, findings, and proposed status.
6. Treat the report's status as evidence-backed advice; the accountable human retains release authority where consequence requires it.

First success is not a green command. It is a bounded evidence package that connects important risks to meaningful oracles, captured executions, findings, residual uncertainty, and a release status no stronger than that proof.

## Deterministic tools

From the installed `software-verification` skill root:

```text
python scripts/inspect_repo.py <repository> --output repo-inventory.json
python scripts/detect_test_stack.py <repository> --output stack.json
python scripts/validate_manifest.py <manifest.json> --root <project-root>
python scripts/validate_traceability.py <manifest.json>
python scripts/scan_test_smells.py <test-path>
python scripts/assemble_report.py <manifest.json> --output verification-report.md
```

See each command's `--help`. Use `scripts/capture_command.py` only after reviewing the explicit command.

The reviewer carries its own manifest and traceability validators. Run it in a fresh context when practical. If it is unavailable, record that the independent challenge was not exercised; same-context self-review is not an equivalent guarantee.

## No skill or shell support

Open `fallback/intake-card.md`, paste `fallback/master-prompt.md`, and run `fallback/review-prompt.md` in a fresh context. Expect copy-ready artifacts, not verified execution.
