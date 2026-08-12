# TestForge: quick start

Use this path to reach a first verification result without confusing a valid package with an installed or healthy host integration.

## Check the package

1. Extract the canonical release ZIP into a new directory.
2. If Python 3.10 or newer is available, open a terminal in the extracted directory and run `python tools/verify_release.py .`. Continue when it returns `"ok": true` with no findings.
3. If Python is unavailable, compare the ZIP's SHA-256 with `TestForge-v1.1.6.zip.sha256` using an operating-system checksum tool. Record the portable verifier as unexecuted. If you cannot perform either check, use only an archive obtained from the canonical GitHub release, retain it unchanged, and treat local package integrity as reduced assurance rather than a pass.
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

1. Confirm the intended TestForge handle is listed by the host and that version `1.1.6` is selected.
2. Name the handle explicitly once to distinguish routing from installation.
3. Confirm the input is a completed candidate for the operator or an existing verification package for the reviewer.
4. Follow [support and recovery](SUPPORT.md), recording package verification, installation, discovery, invocation, and behavior as separate observations.
