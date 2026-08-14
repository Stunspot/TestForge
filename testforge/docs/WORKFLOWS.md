# Verification workflows

## Verify a frozen release candidate

Invoke `$software-verification` with the completed candidate, bounded release claim, target revision, repository, requirements, available evidence, environment, known failures, and authority boundary. Let it inspect the repository before asking questions. Require an impact map, ranked risks, invariants, smallest credible scenario set, oracle rationale, execution plan, and explicit success or stop conditions.

Run only authorized checks in the relevant environment. Capture commands, exit codes, raw outputs, versions, timestamps, and artifact paths. Classify failures as product defects, test defects, environment failures, flaky behavior, or insufficient evidence. Keep designed, written, executed, passed, and interpreted states distinct. Use ordinary working notes while the evidence is changing; assemble the formal verification manifest only at a stable evidence cutoff.

Do not compute custody hashes or checksums, build archives, write package or release receipts, or invoke release-sealing tools during verification. Existing hashes for an already frozen external artifact and checksum behavior under test are narrow exceptions. A non-ready or blocked candidate returns findings only.

For any quota-limited or paid verification route, record a fresh authoritative capacity snapshot and expand the whole planned run before dispatch. Include duplicate triggers, matrix fan-out, retries, runner ceilings, provider billing multipliers, the allowance refresh boundary, and a retained reserve. A hold from `scripts/assess_metered_verification.py` blocks automatic invocation. Paid overage requires a one-shot human authorization bound to the exact execution and plan; technical availability is not permission.

## Challenge the evidence independently

After the operator has produced a manifest, tests, execution records, findings, residual-risk ledger, and proposed status, open a fresh task with `$verification-reviewer`. Supply the complete package and target claim. The reviewer should attack catastrophic omissions, oracle weakness, misleading mocks or fixtures, broken traceability, unsafe testing, and confidence that outruns execution.

Repair material findings in the product, tests, or evidence record, then rerun the affected checks and review. Do not edit a reviewer response into a pass.

## Maintain a quality ratchet

For Augment behavioral evaluations, validate the case envelope, run isolated trials, preserve raw responses and model identity, judge criterion-level evidence, resolve hard gates, and promote only reviewed baselines. Re-run the baseline after prompt, model, tool, package, or trust-boundary changes. A historical pass is not evidence for a changed system.

## Release responsibly

Choose `READY`, `READY_WITH_RESIDUAL_RISK`, `NOT_READY`, `INSUFFICIENT_EVIDENCE`, or `BLOCKED_BY_ENVIRONMENT` only from the retained evidence. Record residual risks, accountable owner, evidence cutoff, unexecuted paths, and rollback or follow-up. TestForge advises; the authorized human or release system makes the consequential release decision.

Only after a ready verdict, completed independent review, explicit release intent, and confirmation that the candidate is unchanged may a separate final-seal process build once, checksum once, and verify once. Any material change voids the seal and requires a new candidate cycle; never repair a stale receipt or generate receipts for receipts.
