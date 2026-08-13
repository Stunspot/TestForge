# TestForge archive custody

TestForge v1.1.7 is one two-skill Augment with several distinct distribution objects. Keep their identity and evidence states separate: source presence is not installation, a valid archive is not discovery, discovery is not invocation, and none of those states proves healthy behavior or directory publication.

## Current v1.1.7 candidate objects

| Object | Canonical location | Observed state and use |
|---|---|---|
| Maintained package | `testforge/` | Current v1.1.7 two-skill source, tools, schemas, examples, evals, adapters, and customer documentation |
| Codex marketplace plugin | `plugins/testforge/` plus `.agents/plugins/marketplace.json` | Repository-native plugin source for `testforge@cd-testforge`; static structure is repository-tested |
| Claude operator upload | `claude-ai/software-verification-v1.1.7.zip` | Current one-skill upload candidate; SHA-256 `41f2d92cf4cf44c91fb6c204364989772ed0c1d0a376c2dfd982d97117da6714` |
| Claude reviewer upload | `claude-ai/verification-reviewer-v1.1.7.zip` | Current one-skill upload candidate; SHA-256 `c882eacec514e23647e1e298b9919a89e3b85ded06649041cf924c91994308ba` |
| Local v1.1.7 customer kit | `releases/v1.1.7/TestForge-v1.1.7.zip` | Deterministic local candidate; the adjacent `.sha256` file is canonical because this document is itself packaged inside the archive |
| Local v1.1.7 receipts | `releases/v1.1.7/` | Static package, source-parity, and portable archive evidence; no fresh-host activation, customer-outcome, tag, GitHub release, or publication claim |
| Source state | Local `main` commits after published v1.1.6 | Release source prepared locally; not tagged, pushed, or published by this maintenance pass |

The current `claude-ai/` archives and the archives inside `releases/v1.1.7/claude/` are separate deterministic builds and are not expected to be byte-identical. Use the current `claude-ai/` objects for repository installation. Use the candidate release directory to inspect the exact evidence and bytes retained for this local release candidate.

## Published v1.1.6 objects

The prior published release remains immutable: Git tag and GitHub release `v1.1.6`, published 2026-08-12. Its frozen customer kit is `releases/v1.1.6/TestForge-v1.1.6.zip`, SHA-256 `4dd052672923192f59ec2866eb2fedef697ca1f98f00a99341c3d8fe062b0594`. Its retained receipts establish static package and byte-parity evidence only.

## OpenAI directory packet

The latest retained skills-only portal payload is still v1.1.4:

- archive: `release-assets/v1.1.4/Plugin-TestForge-v1.1.4-OpenAI-Submission.zip`;
- custody: `release-assets/v1.1.4/openai-submission-custody.json`;
- SHA-256: `9aecec78e407e6f368d0a5c613facbc4252a3f3ef545ba6686e74cf7f2404a46`;
- state: built and repository-tested, not claimed uploaded, approved, published, or discoverable.

There is no retained v1.1.7 portal archive or custody object. The repository-native v1.1.7 plugin is the current local installation candidate; the v1.1.4 portal packet is a separately governed historical submission candidate.

## Maintenance rules

- Rebuild current derivatives from maintained source; never edit ZIP members in place.
- Do not alter historical release directories merely to make present documentation agree with a later release.
- Record archive name, byte size, SHA-256, member inventory, source revision, and claim boundary in the release receipts for each new object.
- Verify extraction topology and package-relative dependencies before publication.
- After publication, download the public asset and compare it with the governed local object.
- Treat upload, automated scan, review submission, approval, publication, installation, discovery, invocation, and health as separate observed states.