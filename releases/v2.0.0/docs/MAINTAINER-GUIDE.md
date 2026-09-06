# TestForge: maintainer guide

Build each release from the maintained repository on a clean release branch. A prior version is evidence, not a template authority.

## Rebuild procedure

1. Finish implementation, repository-native tests, behavioral evaluation, and every document journey declared by `documentation-manifest.json` without running release builders or computing custody hashes.
2. Complete independent skeptical review and resolve its findings. Only a reviewed `READY` or `READY_WITH_RESIDUAL_RISK` candidate proceeds.
3. Freeze the exact candidate on a clean release branch. Confirm `plugins/testforge/skills/` and `testforge/skills/` are identical and the plugin, package, eval suite, and release target declare the same version.
4. Run `python -B tools/build_public_release.py --final-seal` once from the repository root. The explicit flag is accepted only for this post-review sealing phase.
5. Run `python -B releases/v2.0.0/tools/verify_release.py releases/v2.0.0` once and require `ok: true` with no findings.
6. If either final command fails, do not repair manifests or receipts in place. Return the candidate to builder custody, fix it, re-review the changed surface, and start a new final-seal attempt only after it is frozen again.
7. After publication, download the GitHub asset and compare its SHA-256 with the canonical repository artifact and release shelf copy. This is verification of an already released artifact, not construction-time sealing.

## Evidence pointers

- [manifest.json](../manifest.json): exact Codex source-file hashes and Claude archive receipts.
- [verification-report.json](../verification-report.json): portable post-build verification.
- [description-custody.json](../description-custody.json): customer-facing product description custody.
- [package-receipt.json](../package-receipt.json): package identity and static claim boundary.
- [receipt.json](../receipt.json): release identity and evidence boundary.
- `TestForge-v2.0.0.zip.sha256`: detached canonical archive digest.

Never infer installation, discovery, invocation, or healthy behavior from a passing static package check.
