# TestForge: provenance

Each [manifest source record](../releases/v2.0.0/manifest.json) identifies a handle and exact included-file hash inventory without embedding an absolute selected-source path. [Description custody](../releases/v2.0.0/description-custody.json) binds the exact model-visible and UI-short prompt surfaces. [Package verification](../releases/v2.0.0/verification-report.json) binds the assembled Codex and Claude bytes.

## Promotion procedure

1. Verify the selected-source, profile, description, and family-plan inputs named in the [maintainer guide](MAINTAINER-GUIDE.md).
2. Build into a new empty output directory.
3. Run the portable and estate-level verifiers.
4. Preserve the independent review result and detached archive receipt.
5. Promote to the [GitHub custody repository](https://github.com/Stunspot/TestForge) only after all gates pass.

Installation, host discovery, and publication authority remain separate from local package construction.
