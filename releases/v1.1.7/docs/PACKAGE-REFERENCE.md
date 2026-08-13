# TestForge: package reference

## Canonical contents

```text
codex/testforge/
claude/
docs/
tools/verify_release.py
description-custody.json
manifest.json
package-receipt.json
verification-report.json
```

The canonical archive is `TestForge-v1.1.7.zip`. The release tree contains `receipt.json`. The `.sha256` file lives beside the archive because an archive cannot contain its own final digest.

## Key records

- [Plugin manifest](../codex/testforge/.codex-plugin/plugin.json)
- [Release manifest](../manifest.json)
- [Description custody](../description-custody.json)
- [Portable verification report](../verification-report.json)
- [Package receipt](../package-receipt.json)
- [Validation procedure](VALIDATION.md)

The Software Verification skill includes `assets/templates/metered-verification-plan.json`, its exact field contract at `assets/schemas/metered-verification-plan.schema.json`, and the five-field output contract at `assets/templates/metered-verification-response.md`.
