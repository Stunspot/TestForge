# Verification workflows

## Verify a change or release candidate

Invoke `$software-verification` with the requirement, repository or diff, target revision, environment, known failures, and authority boundary. Let it inspect the repository before asking questions. Require an impact map, ranked risks, invariants, smallest credible scenario set, oracle rationale, execution plan, and explicit success or stop conditions.

Run only authorized checks in the relevant environment. Capture commands, exit codes, raw outputs, versions, timestamps, and artifact paths. Classify failures as product defects, test defects, environment failures, flaky behavior, or insufficient evidence. Keep designed, written, executed, passed, and interpreted states distinct.

## Challenge the evidence independently

After the operator has produced a manifest, tests, execution records, findings, residual-risk ledger, and proposed status, open a fresh task with `$verification-reviewer`. Supply the complete package and target claim. The reviewer should attack catastrophic omissions, oracle weakness, misleading mocks or fixtures, broken traceability, unsafe testing, and confidence that outruns execution.

Repair material findings in the product, tests, or evidence record, then rerun the affected checks and review. Do not edit a reviewer response into a pass.

## Maintain a quality ratchet

For Augment behavioral evaluations, validate the case envelope, run isolated trials, preserve raw responses and model identity, judge criterion-level evidence, resolve hard gates, and promote only reviewed baselines. Re-run the baseline after prompt, model, tool, package, or trust-boundary changes. A historical pass is not evidence for a changed system.

## Release responsibly

Choose `READY`, `READY_WITH_RESIDUAL_RISK`, `NOT_READY`, `INSUFFICIENT_EVIDENCE`, or `BLOCKED_BY_ENVIRONMENT` only from the retained evidence. Record residual risks, accountable owner, evidence cutoff, unexecuted paths, and rollback or follow-up. TestForge advises; the authorized human or release system makes the consequential release decision.
