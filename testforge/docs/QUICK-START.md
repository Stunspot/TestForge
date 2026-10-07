# Quick start

## Install

Each v2.0.0 skill is self-contained. Python 3.10+ is required only for deterministic scripts; TestForge has no mandatory third-party package dependency.

Use [Install in Codex](INSTALL-CODEX.md) or [Install in Claude](INSTALL-CLAUDE.md). Install and verify both skills separately. Structural validation proves the package shape; successful discovery requires a fresh host task or conversation.

### Claude Code

Copy both complete skill directories into `~/.claude/skills/` for personal use or `.claude/skills/` for one project. Invoke `/software-verification` and `/verification-reviewer` when explicit selection is useful.

## First verification

1. Invoke `$software-verification` with a completed frozen candidate, its target revision, bounded release claim, and available evidence.
2. Let it inspect existing manifests, tests, and conventions before answering questions. Use ordinary working notes while risks, tests, and failures are still changing.
3. Review any proposed command or repository edit. Approve consequential actions only within a bounded scope.
4. At a stable evidence cutoff, assemble the verification manifest once in the target project's working area, not inside this installed package.
5. Run `$verification-reviewer` with the completed manifest, tests, evidence, findings, and proposed status.
6. Treat the report's status as evidence-backed advice; the accountable human retains release authority where consequence requires it.
7. Do not build release archives, compute custody checksums, or write package or release receipts until the verdict and independent review are complete. A separate final release process may seal an unchanged `READY` or `READY_WITH_RESIDUAL_RISK` candidate once.

Before hosted CI, device farms, browser farms, or any other finite or paid test service, require a current capacity observation for the exact account that will be charged. Count the complete run—including duplicate triggers, matrix jobs, retries, runner ceilings, and billing multipliers—then retain a human-set reserve. If capacity is unknown, stale, across its refresh boundary, or insufficient, TestForge holds the hosted run and proposes the smallest credible local, clean-host, self-hosted, or batched substitute. It never launches a job just to ask the meter whether the job was affordable.

First success is not a green command. It is a bounded evidence package that connects important risks to meaningful oracles, captured executions, findings, residual uncertainty, and a release status no stronger than that proof.

## Deterministic tools

From the installed `software-verification` skill root:

```text
python scripts/inspect_repo.py <repository> --output repo-inventory.json
python scripts/detect_test_stack.py <repository> --output stack.json
python scripts/validate_manifest.py <manifest.json> --root <project-root>
python scripts/validate_traceability.py <manifest.json>
python scripts/scan_test_smells.py <test-path>
python scripts/assess_metered_verification.py <metered-plan.json>
python scripts/assemble_report.py <manifest.json> --output verification-report.md
```

See each command's `--help`. Use `scripts/capture_command.py` only after reviewing the explicit command.

For the metered preflight, copy `assets/templates/metered-verification-plan.json` into the target project's working area and replace every example identity, timestamp, allowance, reserve, and expanded job with a current observation and the exact planned run. The full field contract is `assets/schemas/metered-verification-plan.schema.json`. Format the decision with `assets/templates/metered-verification-response.md`. The assessor can permit included-capacity execution or hold a route; it cannot authenticate human authority or permit paid dispatch.

The reviewer carries its own manifest and traceability validators. Run it in a fresh context when practical. If it is unavailable, record that the independent challenge was not exercised; same-context self-review is not an equivalent guarantee.

## No skill or shell support

Open `fallback/intake-card.md`, paste `fallback/master-prompt.md`, and run `fallback/review-prompt.md` in a fresh context. Expect copy-ready artifacts, not verified execution.


## Submit the outcome you actually need verified

Include the candidate location/revision, advertised user promise, intended user, real starting point, representative data and authorized environment. Explain what must survive interruption or return. Existing test logs help, but they do not choose the product's acceptance criteria for you.

For an archive or learning product, this is a useful request:

> Verify this candidate from its actual landing page. A new reader must discover a relevant subject without already knowing a search term, choose material from a meaningful preview, open it, return to the same results, and resume saved work. A learner must recognize the subject, first lesson, sequence and meaning of progress. Inspect the supported themes on the controls and panels actually used. Report the steps and outcomes you observed; keep participant usability and untested assistive technology separate.

A report that tests only imports, HTTP success or whether a button exists supports that narrow scope. It does not establish the complete discovery, learning and resumption experience. If the candidate fails, retain the finding, repair in builder custody and submit the changed candidate for a fresh bounded verification cycle.

## Recover from incomplete or contradictory test output

Retain the original output. `normalize_test_results.py` reports `unparsed` when the input is unsupported, empty, entirely skipped or contradicts its declared totals. An observed testcase failure remains a failure even if suite totals omit it. A normalized command pass requires exit code zero. The normalization command returning zero means parsing succeeded; inspect `summary.status` to determine whether tests passed or failed.

Use `validate_manifest.py` and `validate_traceability.py` before assembling a report. A ready verdict needs a candidate-bound evidence chain, actual command or observational records, an identified independent review, every decision-critical check passed and no open material product defect. A passing individual case inside a failed combined run needs its own `case_evidence` locator; the combined run still cannot support a ready verdict. Repair the record from retained evidence rather than changing the status to satisfy the validator. When evidence cannot be recovered, keep `INSUFFICIENT_EVIDENCE` or the appropriate environment-limited status.

## Readiness, observations and review conditions

A technical READY applies only to the included claim; it grants no release authority. Required unexecuted checks cannot be waived by a residual-risk label. An optional unfinished check needs a specific residual record with its owner and revisit condition. An open blocking reviewer condition prevents readiness.

A browser walkthrough or supplied observation does not need a fabricated shell command. Record its procedure, actual observed result, recorder, source, environment, candidate revision and raw evidence locator using the observation form in the installed skill's references/core/evidence-records.md. Commands retain their real exit codes. The report assembler checks local evidence relative to the manifest directory; use --evidence-root when the retained evidence lives elsewhere.

Preserve failed attempts. One proven support failure may be superseded by a successful correction tied to the same candidate and resolved cause; a product defect cannot use that exception. A deliberately failing mutant is a separate specimen that tests oracle strength. Keep its expected result separate from the legitimate candidate's result.

If a local model emits contradictory verdicts or invents evidence, that configuration has not qualified the judgment. Retain the raw response and use independent review or another already-authorized capable route. Do not keep rewriting the rubric or discarding cases until the output appears to pass.


Support recovery must identify the same tests on both attempts. Nonempty execution.test_ids bind the failed scope and its replacement; every failed check must now point to that passing replacement. Missing old scope remains unknown. A passing health check cannot replace a failed restore check, although a corrected interpreter may rerun the restore check.
