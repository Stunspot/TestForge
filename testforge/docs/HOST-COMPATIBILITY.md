# Host compatibility

## Distribution contract

TestForge v1.1.0 has two independent skills:

| Skill | Purpose | Codex unit | Claude.ai unit |
|---|---|---|---|
| `software-verification` | risk-ranked verification through evidence-backed release assessment | complete skill folder | `software-verification-v1.1.0.zip` |
| `verification-reviewer` | independent challenge of the evidence chain | complete skill folder | `verification-reviewer-v1.1.0.zip` |

Each skill contains every runtime file referenced by its `SKILL.md`. The operator includes doctrine, templates, examples, fallbacks, and deterministic utilities. The reviewer includes its rubric, adversarial checks, and required structural validators. No installed skill depends on a parent package path.

## Verified structure

- Both source skill folders pass the current Augment Builder Codex and Claude profiles.
- Each Claude archive has portable forward-slash members and exactly one top-level skill folder.
- Each extracted Claude skill matches its source skill folder byte-for-byte.
- The package's deterministic tests, package verifier, and behavioral-evaluation envelope validation pass.

## Activation boundary

Structural readiness does not establish live host behavior. Fresh Codex discovery for this version, Claude.ai upload and enablement, Claude progressive resource loading, script execution, reviewer handoff, and persistence were not exercised during the v1.1.0 packaging pass. Claude Code execution also remains unrecorded. Preserve those states as unexecuted, not failed and not passed.
