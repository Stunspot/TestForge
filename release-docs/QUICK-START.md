# TestForge: quick start

Use this path to reach a first verification result without confusing a valid package with an installed or healthy host integration.

## Check the package

1. Extract the canonical release ZIP into a new directory.
2. If Python 3.10 or newer is available, open a terminal in the extracted directory and run `python tools/verify_release.py .`. Continue when it returns `"ok": true` with no findings.
3. If Python is unavailable, compare the ZIP's SHA-256 with a separately supplied canonical digest when available, using an operating-system checksum tool. Record the portable verifier as unexecuted. If you cannot perform either check, use only an archive obtained from the canonical GitHub release, retain it unchanged, and treat local package integrity as reduced assurance rather than a pass.
4. Complete the [Codex installation](INSTALL-CODEX.md) or [Claude installation](INSTALL-CLAUDE.md), then start a fresh task or chat.

## First value: verify a completed candidate

Invoke `$software-verification` with a completed candidate, its bounded readiness claim, and the available evidence. Copy this prompt:

> $software-verification Verify this completed candidate for release. Bind the target and revision, rank the consequential risks, connect each scenario to an oracle and execution evidence, report findings and residual risk, and issue one bounded TestForge verdict.

A useful result identifies the target/revision, risks, scenarios, oracles, executed versus unexecuted evidence, findings, residual risk, and exactly one supported status. If the submission is unfinished, `INSUFFICIENT_EVIDENCE` or `NOT_READY` is a successful TestForge result—not an invitation for TestForge to finish the product.

Before hosted CI, device farms, browser farms, or another finite or paid test service, require a current capacity observation for the exact account that will be charged. Copy `assets/templates/metered-verification-plan.json` from the installed Software Verification skill and replace its examples with the exact observation and run. The field contract is `assets/schemas/metered-verification-plan.schema.json`; format the decision with `assets/templates/metered-verification-response.md`. Count duplicate triggers, matrix jobs, retries, runner ceilings, and billing multipliers, and retain a human-set reserve. A hold means do not launch that route; use a credible local, clean-host, self-hosted, or batched substitute when it tests the needed boundary. The assessor cannot authenticate human authority or permit paid dispatch.

## First value: challenge the evidence

After a verification package exists, start a fresh context when practical and copy:

> $verification-reviewer Challenge this verification package. Check revision binding, catastrophic-risk coverage, oracle quality, executed evidence, finding closure, residual risk, and whether the stated TestForge verdict is supported.

A useful review returns an independent review verdict, actionable findings or an explicit clean disposition, and the closure required before release. If no verification package exists yet, the correct result is a bounded request for one; the reviewer does not invent upstream evidence.

## If first value does not appear

1. Confirm the intended TestForge handle is listed by the host and that version `2.0.0` is selected.
2. Name the handle explicitly once to distinguish routing from installation.
3. Confirm the input is a completed candidate for the operator or an existing verification package for the reviewer.
4. Follow [support and recovery](SUPPORT.md), recording package verification, installation, discovery, invocation, and behavior as separate observations.

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
