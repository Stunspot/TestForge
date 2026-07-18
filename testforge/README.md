# TestForge: Software Verification Operator

Turn a software change, repository, failing test, or feature requirement into risk-ranked, repository-compatible verification evidence—and a release conclusion that says what is still unsafe to ship.

TestForge is a portable Augment with one self-contained verification operator, one self-contained independent reviewer, progressive testing doctrine, operational artifacts, deterministic Python tools, TypeScript/Python stack guidance, three situated examples, behavioral evaluations, and a fileless fallback. Markdown is the canonical human record; JSON is the canonical machine record.

## Start here

1. Read `docs/QUICK-START.md`.
2. Install `skills/software-verification` and `skills/verification-reviewer` as complete skill folders, or upload the matching one-skill archives from the repository's `claude-ai/` directory.
3. Invoke `$software-verification` with whatever you have: a diff, repository, defect, test failure, requirement, or release candidate.
4. Let TestForge inspect before it questions you. It asks only for decision-critical information it cannot recover.
5. Run the independent reviewer before accepting a release assessment.

## Principal entry points

- `skills/software-verification/SKILL.md` — scope through evidence-backed release assessment.
- `skills/verification-reviewer/SKILL.md` — independent challenge of the evidence chain.
- `assets/templates/verification-manifest.json` — canonical working record.
- `scripts/` — repository inspection, stack detection, diff summary, validation, normalization, smell scanning, and report assembly.
- `examples/` — complete TypeScript API, Python regression, and parser-edge demonstrations.
- `evals/` — transfer-oriented cases for risk, oracle, evidence, triage, and safety behavior.
- `fallback/master-prompt.md` — copy-paste operation when skill loading or repository tools are unavailable.

## Honest capability boundary

TestForge uses the files and tools a host actually exposes. It can create compatible tests and run repository-local checks when execution is available and authorized; it cannot grant file access, install dependencies, create environments, certify compliance, prove defect-freedom, or assume release authority. Active security testing, destructive operations, production access, dependency installation, production-code modification, CI changes, and external publication remain human-authorized actions.

See `docs/CAPABILITY-MATRIX.md`, `docs/LIMITATIONS.md`, and `SECURITY.md` for the exercised boundary. See `docs/HOST-COMPATIBILITY.md` for the exact Codex, Claude.ai, and Claude Code installation units.
