# TestForge v1.1.1 archive custody

TestForge is one two-skill Augment with several independently useful release objects. The canonical release keeps the complete product, its Codex plugin, and both standalone skills separately obtainable without pretending that a standalone skill is the whole product.

| Object | Canonical release artifact | Use |
|---|---|---|
| Complete Augment | `release-assets/v1.1.1/TestForge-v1.1.1.zip` | Portable two-skill TestForge capability with adapters, docs, evals, and tools |
| Codex plugin | `release-assets/v1.1.1/Plugin-TestForge-v1.1.1.zip` | Branded Codex plugin with both skill entry points and listing assets |
| Software Verification skill | `release-assets/v1.1.1/Skill-software-verification--TestForge-v1.1.1.zip` | Independent `$software-verification` installation and recovery |
| Verification Reviewer skill | `release-assets/v1.1.1/Skill-verification-reviewer--TestForge-v1.1.1.zip` | Independent `$verification-reviewer` installation and recovery |
| Claude.ai uploads | `claude-ai/software-verification-v1.1.1.zip` and `claude-ai/verification-reviewer-v1.1.1.zip` | Host-specific one-skill upload archives |
| Source repository | Git tag `v1.1.1` and its GitHub source archives | Versioned source, documentation, tests, testbed, and provenance |

`release-assets/v1.1.1/archive-custody.json` records exact hashes, sizes, member counts, source-tree digests, and extraction-parity results for the governed archives. GitHub release assets and the latest-only convenience backup shelf must match those hashes. Canonical assets are copied, never moved, to the backup shelf. Older same-family convenience copies may be removed only after the new copies match; unrelated products are untouched.

The two standalone skill archives and their Claude.ai counterparts intentionally carry the same skill content under channel-appropriate names. Static package equality does not establish live Claude activation, live Codex discovery, or directory approval.

