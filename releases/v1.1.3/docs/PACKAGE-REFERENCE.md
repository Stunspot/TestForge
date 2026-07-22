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

The canonical archive is `TestForge-v1.1.3.zip`. Its detached `receipt.json` and `.sha256` file live beside it in the repository or staging tree because an archive cannot contain its own final digest.

## Key records

- [Plugin manifest](../codex/testforge/.codex-plugin/plugin.json)
- [Release manifest](../manifest.json)
- [Description custody](../description-custody.json)
- [Portable verification report](../verification-report.json)
- [Package receipt](../package-receipt.json)
- [Validation procedure](VALIDATION.md)
