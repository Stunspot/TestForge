# TestForge: maintainer guide

Build each release from the maintained repository on a clean release branch. A prior version is evidence, not a template authority.

## Rebuild procedure

1. Confirm `plugins/testforge/skills/` and `testforge/skills/` are byte-identical and the plugin, package, eval suite, and release target all declare version `1.1.6`.
2. Run `python -B tools/build_public_release.py` from the repository root.
3. Run it a second time and require the same SHA-256 digest.
4. Run `python -B releases/v1.1.6/tools/verify_release.py releases/v1.1.6` and require `ok: true` with no findings.
5. Run the repository unit suites, package validator, eval-suite validator, release-manifest validator, and line-ending verifier.
6. Review all thirteen customer documents as a reader journey, including installation, first value, expected success, troubleshooting, removal, and rollback.
7. Require an independent skeptical review before publication.
8. After publication, download the GitHub asset and compare its SHA-256 with the canonical repository artifact and release shelf copy.

## Evidence pointers

- [manifest.json](../manifest.json): exact Codex source-file hashes and Claude archive receipts.
- [verification-report.json](../verification-report.json): portable post-build verification.
- [description-custody.json](../description-custody.json): customer-facing product description custody.
- [package-receipt.json](../package-receipt.json): package identity and static claim boundary.
- [receipt.json](../receipt.json): release identity and evidence boundary.
- `TestForge-v1.1.6.zip.sha256`: detached canonical archive digest.

Never infer installation, discovery, invocation, or healthy behavior from a passing static package check.
