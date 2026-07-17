# TestForge v1.0.0

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
