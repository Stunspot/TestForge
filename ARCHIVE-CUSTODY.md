# TestForge archive custody

TestForge is one two-skill Augment with several independently useful release objects. The canonical release keeps the complete product, its Codex plugin, and both standalone skills separately obtainable without pretending that a standalone skill is the whole product.

| Object | Canonical release artifact | Use |
|---|---|---|
| Complete Augment | `release-assets/v1.1.1/TestForge-v1.1.1.zip` | Portable two-skill TestForge capability with adapters, docs, evals, and tools |
| Codex plugin | `release-assets/v1.1.1/Plugin-TestForge-v1.1.1.zip` | Branded Codex plugin with both skill entry points and listing assets |
| Software Verification skill | `release-assets/v1.1.1/Skill-software-verification--TestForge-v1.1.1.zip` | Independent `$software-verification` installation and recovery |
| Verification Reviewer skill | `release-assets/v1.1.1/Skill-verification-reviewer--TestForge-v1.1.1.zip` | Independent `$verification-reviewer` installation and recovery |
| Claude.ai uploads | `claude-ai/software-verification-v1.1.1.zip` and `claude-ai/verification-reviewer-v1.1.1.zip` | Host-specific one-skill upload archives |
| Source repository | Git tag `v1.1.1` and its GitHub source archives | Versioned source, documentation, tests, testbed, and provenance |

## Plugin publication payloads

TestForge plugin v1.1.2 preserves two deliberately different ZIPs:

| Object | Canonical release artifact | Use |
|---|---|---|
| Installable Codex plugin | `release-assets/v1.1.2/Plugin-TestForge-v1.1.2.zip` | Normal Codex installation and marketplace distribution with the full interface manifest |
| OpenAI skills-only submission | `release-assets/v1.1.2/Plugin-TestForge-v1.1.2-OpenAI-Submission.zip` | Deterministic portal upload whose archived interface retains only `composerIcon` and `logo` |

`release-assets/v1.1.2/archive-custody.json` governs the installable plugin. `release-assets/v1.1.2/openai-submission-custody.json` separately records the portal derivative's archive hash, source and transformed manifest hashes, member count, and POSIX path requirement. The portal ZIP is not a replacement for the installable plugin.

`release-assets/v1.1.1/archive-custody.json` records exact hashes, sizes, member counts, source-tree digests, and extraction-parity results for the unchanged v1.1.1 Augment and skills. GitHub release assets and the latest-only convenience backup shelf must match the applicable custody records. Canonical assets are copied, never moved, to the backup shelf. Older same-family convenience copies may be removed only after the new copies match; unrelated products are untouched.

The two standalone skill archives and their Claude.ai counterparts intentionally carry the same skill content under channel-appropriate names. Static package equality does not establish live Claude activation, live Codex discovery, or directory approval.
