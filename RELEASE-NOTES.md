# TestForge v1.0.1

Version 1.0.1 turns the Build Week evaluation loop back onto TestForge itself. A matched Qwen control/treatment run improved from 72.08 to 88.33 but retained one indispensable evidence-honesty failure: the model proposed removing a system package to reproduce a missing-library condition. This revision strengthens safe, read-only, capability-matched diagnosis and cleanly separates executed commands, proposed diagnostics, and unexecuted remediation. It also prevents a judge from hiding weak observable performance by mislabeling it as an invalid episode.

Repeated test-diagnose-reengineer cycles then exposed and repaired context dilution, secret-workflow leakage into unrelated cases, incomplete authorization post-state checks, unsafe production-probe scaffolds, destructive-deletion authority gaps, and local-judge logic inversions. A later full local run reached 90.41 with zero failed or invalid episodes; single-trial behavioral results remain model-, context-, and judge-bounded.

It also adds repository-native Codex plugin installation, Build Week provenance, an isolated fictional judge case, public distribution-integrity tests, and a three-operating-system CI matrix.

## Original v1.0.0 release

TestForge is a free Collaborative Dynamics Augment that gives an Agent two complementary software-verification capabilities:

- `$software-verification` builds a risk-ranked evidence chain from change to release assessment.
- `$verification-reviewer` independently challenges that chain for omissions, weak oracles, misleading mocks and unsupported confidence.

The repository also includes the CD Augment evaluation testbed for running isolated behavioral cases against Codex or local Ollama models, preserving hard gates and promoting reviewed regression baselines.

## Included

- complete portable TestForge Augment;
- two Agent SKILLs and copy-paste fallbacks;
- deterministic Python inspection, validation, normalization and reporting tools;
- Python and TypeScript worked examples with planted defects;
- risk, oracle, reliability, security and stack references;
- canonical behavioral eval suite;
- isolated Augment evaluation harness with Codex and Ollama adapters;
- reviewed compact baselines;
- Codex, Claude Code, GitHub, local-shell and plain-chat adapters.

## License

The release uses a split license: MIT for Python software and machine-readable schemas, and CC BY-ND 4.0 for authored Augment materials. The authentic, unmodified branded Augment may be redistributed, including inside a larger commercial product. See `LICENSE.md`, `ATTRIBUTION.md` and `TRADEMARKS.md`.

## Evidence boundary

The package and testbed deterministic suites pass locally. Supplied behavioral baselines record their model and context. TestForge provides evidence-bounded advice; it does not prove defect freedom, certify compliance or authorize a release.
