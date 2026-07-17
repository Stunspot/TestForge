![TestForge - software verification that argues back](assets/testforge-social-preview.png)

# TestForge

TestForge is a free Collaborative Dynamics Augment for turning software changes, repositories, defects and release candidates into risk-ranked verification evidence instead of a comforting pile of green checkmarks.

It includes two Agent SKILLs:

- `$software-verification` reconstructs impact, ranks failure risk, designs meaningful oracles, creates stack-compatible tests, interprets execution evidence and issues a traceable release assessment.
- `$verification-reviewer` independently attacks the evidence chain for catastrophic omissions, weak tests, unsupported claims and verdicts that outrun the proof.

This repository also includes the CD Augment evaluation testbed used to run isolated behavioral cases, keep answer keys away from the evaluated model, record criterion-level judgments, preserve hard gates outside the average and promote reviewed regression baselines.

## What you can do with it

- Hand an Agent a bug, diff, feature or failing test and get a risk-driven verification plan.
- Generate tests that try to expose consequential failure rather than merely exercise edited lines.
- Distinguish product defects, test defects, environment failures, flaky behavior and insufficient evidence.
- Produce `READY`, `READY_WITH_RESIDUAL_RISK`, `NOT_READY`, `INSUFFICIENT_EVIDENCE` or `BLOCKED_BY_ENVIRONMENT` with a reproducible evidence trail.
- Challenge that conclusion with a separate skeptical reviewer.
- Run and track behavioral evals for other Augments with Codex or local Ollama models.

TestForge is advisory verification machinery. It does not prove defect freedom, certify compliance, grant production access, authorize release, or turn model confidence into evidence.

## Repository map

- [`testforge/`](testforge/) - the complete portable TestForge Augment v1.0.0.
- [`testforge/docs/QUICK-START.md`](testforge/docs/QUICK-START.md) - install and first-use guide.
- [`testforge/docs/SALES-DEMO.md`](testforge/docs/SALES-DEMO.md) - a compact proof-of-value scenario.
- [`tools/augment-evals/`](tools/augment-evals/) - isolated Augment behavioral evaluation harness.
- [`tools/augment-evals/README.md`](tools/augment-evals/README.md) - testbed setup, run, review, seal, promote and regression workflow.

## Quick start: use the Agent SKILLs

Download the latest release, unzip it and keep the `testforge/` tree together. Expose both directories under `testforge/skills/` through your Agent host's skill mechanism. Host-specific notes are included for [Codex](testforge/adapters/codex.md), [Claude Code](testforge/adapters/claude-code.md), [GitHub](testforge/adapters/github.md), [local shell](testforge/adapters/local-shell.md) and [copy-paste chat](testforge/adapters/copy-paste-chat.md).

Then start with:

```text
$software-verification Verify this change. Reconstruct what could break, create the smallest credible evidence set, run only safe authorized checks, and give me an evidence-backed release assessment.
```

After the evidence package exists, use a fresh context when practical:

```text
$verification-reviewer Challenge this verification package and tell me whether its release status is actually supported.
```

Python 3.10+ is needed only for deterministic tools. The TestForge package itself has no mandatory third-party Python dependency.

## Quick start: run Augment behavioral evals

From the repository root:

```powershell
py -m pip install -r tools\augment-evals\requirements.txt
py tools\augment-evals\augment_eval.py validate testforge
```

Then choose a supplied adapter or create one using the documented adapter contract. Local Ollama and signed-in Codex CLI examples are included. Raw runs remain local under `evaluation-results/`; reviewed compact baselines can be promoted into Git-tracked records.

## Trust and evidence

The release contains synthetic planted-defect examples, deterministic package tooling, canonical eval cases and reviewed local baselines. Read the exact exercised and unexercised boundaries in [`testforge/docs/LIMITATIONS.md`](testforge/docs/LIMITATIONS.md), [`testforge/SECURITY.md`](testforge/SECURITY.md) and the testbed README.

Do not send secrets or unnecessary proprietary code in an issue. Active security testing, destructive operations, production access, dependency installation, production-code changes, CI changes and external publication remain explicitly authorized human decisions.

## License

TestForge uses a split license: MIT for Python software and machine-readable schemas, and CC BY-ND 4.0 for the authored Augment materials. You may redistribute the authentic, unmodified branded Augment, including inside a larger commercial product. See [`LICENSE.md`](LICENSE.md), [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`TRADEMARKS.md`](TRADEMARKS.md).

## Publisher

TestForge is a Collaborative Dynamics Augment. Issues and contributions are welcome under the boundaries in [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md).
