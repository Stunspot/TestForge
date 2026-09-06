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

The canonical archive is `TestForge-v2.0.0.zip`. The release tree contains `receipt.json`. The `.sha256` file lives beside the archive because an archive cannot contain its own final digest.

## Key records

- [Plugin manifest](../releases/v2.0.0/codex/testforge/.codex-plugin/plugin.json)
- [Release manifest](../releases/v2.0.0/manifest.json)
- [Description custody](../releases/v2.0.0/description-custody.json)
- [Portable verification report](../releases/v2.0.0/verification-report.json)
- [Package receipt](../releases/v2.0.0/package-receipt.json)
- [Validation procedure](VALIDATION.md)

The Software Verification skill includes `assets/templates/metered-verification-plan.json`, its exact field contract at `assets/schemas/metered-verification-plan.schema.json`, and the five-field output contract at `assets/templates/metered-verification-response.md`.

## 2.0.0 assessor compatibility

The assessor no longer emits `plan_sha256`. Callers migrating from the original 1.1.7 archive must stop requiring that output field. A trusted dispatcher must bind paid authority to the exact execution and complete canonical plan content. The assessor never grants paid dispatch.
