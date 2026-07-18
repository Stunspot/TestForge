# TestForge judge quickstart

This path takes about five minutes, uses fictional code, and requires no API key, hosted service, private repository, or test account.

## 1. Install the Codex plugin

From a terminal with Codex installed:

```text
codex plugin marketplace add Stunspot/TestForge
codex plugin add testforge@cd-testforge
```

Start a new Codex task after installation. The plugin adds two Agent SKILLs:

- `$software-verification`
- `$verification-reviewer`

## 2. Isolate the fictional release candidate

Copy `judge-fixture/tenant-access/` into a separate temporary folder, then open only that copied folder in Codex. Keeping the fixture separate prevents the Agent from seeing this quickstart's expected observations.

The supplied three-test suite is green:

```text
python -m unittest discover -v
```

## 3. Ask TestForge to verify it

Send this in the new Codex task:

```text
$software-verification

Verify this small repository as a release candidate. Reconstruct what the access-policy change could break, compare the implementation and tests with requirement.md, run safe local checks, create the smallest additional evidence needed, and give me an evidence-backed release assessment.
```

Approve only safe local inspection, test creation, and test execution inside the copied fixture.

## Expected observations

A strong TestForge run should:

- treat the written requirement as the policy oracle rather than assuming three green tests are enough;
- identify cross-tenant editing as the critical authorization risk;
- add or propose a test where an editor from another tenant attempts to edit the document;
- expose that the current implementation authorizes the cross-tenant editor;
- distinguish the product defect from the pre-existing suite's coverage gap;
- issue `NOT_READY` or an equivalently bounded non-release conclusion supported by actual execution;
- avoid claiming any test ran unless command evidence exists.

## 4. Challenge the result

When the operator has produced its manifest, tests, evidence, findings, and proposed status, start a fresh Codex task when practical and send:

```text
$verification-reviewer

Independently challenge the verification package in this workspace. Look for a missed catastrophic risk, a weak oracle, misleading mock or fixture evidence, broken traceability, unsafe testing, or a release status more confident than the execution record allows.
```

The reviewer should assess the evidence rather than merely agree with the operator.

## Deterministic repository checks

To exercise the public package without a model:

```text
python -m pip install -r tools/augment-evals/requirements.txt
python -m unittest discover -s testforge/tests -v
python -m unittest discover -s tools/augment-evals/tests -v
python -m unittest discover -s tests -v
python testforge/scripts/verify_package.py testforge
python testforge/scripts/verify_package.py plugins/testforge/skills/software-verification/testforge
python tools/augment-evals/augment_eval.py validate testforge
```

Python 3.10 or newer is required. PyYAML is the testbed's only third-party dependency; the TestForge Augment's deterministic tools use the standard library.

## Supported paths

- Codex plugin: repository-native two-command installation above.
- Codex standalone SKILLs: install the portable `testforge/` bundle while preserving package-relative resources.
- Claude Code: structurally compatible SKILL instructions with documented host boundaries.
- Other Agent hosts: Markdown skill loading, local-shell adapter, GitHub adapter, or copy-paste fallback.

See `testforge/docs/SUPPORTED-ENVIRONMENTS.md` and `testforge/docs/LIMITATIONS.md` for the exact exercised boundary.
