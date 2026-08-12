# TestForge archive custody

TestForge v1.1.6 is one two-skill Augment with several distinct distribution objects. Keep their identity and evidence states separate: source presence is not installation, a valid archive is not discovery, discovery is not invocation, and none of those states proves healthy behavior or directory publication.

## Current v1.1.6 objects

| Object | Canonical location | Observed state and use |
|---|---|---|
| Maintained package | `testforge/` | Current two-skill source, tools, schemas, examples, evals, adapters, and customer documentation |
| Codex marketplace plugin | `plugins/testforge/` plus `.agents/plugins/marketplace.json` | Repository-native plugin source for `testforge@cd-testforge`; static structure is repository-tested |
| Claude operator upload | `claude-ai/software-verification-v1.1.6.zip` | Current one-skill upload archive; SHA-256 `3485f982d9d7f770b9077bc9da122498ff5ce135ae60e07e7aa8fa8209d5a52f` |
| Claude reviewer upload | `claude-ai/verification-reviewer-v1.1.6.zip` | Current one-skill upload archive; SHA-256 `c882eacec514e23647e1e298b9919a89e3b85ded06649041cf924c91994308ba` |
| Frozen v1.1.6 customer kit | `releases/v1.1.6/TestForge-v1.1.6.zip` | Canonical published release object retained unchanged; SHA-256 `4dd052672923192f59ec2866eb2fedef697ca1f98f00a99341c3d8fe062b0594` |
| Frozen v1.1.6 receipts | `releases/v1.1.6/` | Static package, source-parity, and portable archive evidence; no fresh-host activation or customer-outcome claim |
| Source release | Git tag `v1.1.6` and [GitHub release](https://github.com/Stunspot/TestForge/releases/tag/v1.1.6) | Published 2026-08-12; versioned public source and release boundary |

The current `claude-ai/` archives and the frozen archives inside `releases/v1.1.6/claude/` are separate deterministic builds and are not byte-identical. Use the current `claude-ai/` objects for the repository installation guide. Use the frozen release directory to inspect the exact evidence and bytes retained for the v1.1.6 release event.

## OpenAI directory packet

The latest retained skills-only portal payload is still v1.1.4:

- archive: `release-assets/v1.1.4/Plugin-TestForge-v1.1.4-OpenAI-Submission.zip`;
- custody: `release-assets/v1.1.4/openai-submission-custody.json`;
- SHA-256: `9aecec78e407e6f368d0a5c613facbc4252a3f3ef545ba6686e74cf7f2404a46`;
- state: built and repository-tested, not claimed uploaded, approved, published, or discoverable.

There is no retained v1.1.6 portal archive or custody object. The repository-native v1.1.6 plugin remains the current Codex installation surface; the v1.1.4 portal packet is a separately governed historical submission candidate.

## Maintenance rules

- Rebuild current derivatives from maintained source; never edit ZIP members in place.
- Do not alter `releases/` merely to make present documentation agree with a historical release.
- Record archive name, byte size, SHA-256, member inventory, source revision, and claim boundary for each new object.
- Verify extraction topology and package-relative dependencies before publication.
- After publication, download the public asset and compare it with the governed local object.
- Treat upload, automated scan, review submission, approval, publication, installation, discovery, invocation, and health as separate observed states.