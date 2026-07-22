# Install TestForge in Codex

## Prerequisites

- An extracted `TestForge-v1.1.3.zip` release.
- A Codex build that supports local plugin import or a configured local plugin source directory.
- Permission to add a local plugin on the host.

## Procedure

1. From the extracted release root, run `python tools/verify_release.py .` and require `"ok": true`.
2. Confirm the payload contains [plugin.json](../codex/testforge/.codex-plugin/plugin.json) and a `codex/testforge/skills/` directory.
3. In Codex's supported local-plugin import flow, select the complete `codex/testforge/` directory. If the host instead uses a configured plugin source directory, copy that whole directory there unchanged; do not copy individual skill files out of it.
4. Let Codex reload plugins, then open a fresh task so discovery is tested without stale task state.
5. Confirm `TestForge` and its expected handles are listed by the host.
6. Use the starter prompt from the [quick start](QUICK-START.md).

## Expected success

- The host reports the plugin as installed or loaded.
- A fresh task can discover the expected handle.
- An explicit invocation reaches the requested capability without package or manifest errors.

These are three separate observations. Do not call the plugin healthy merely because its files were copied.

## Recovery

1. If static verification fails, discard the extracted copy and extract again from the canonical ZIP.
2. If verification passes but the plugin is absent, confirm the host supports local plugins and that the selected directory is `codex/testforge/`, not its parent or `skills/` child.
3. If an older duplicate is selected, preserve it until its provenance is known; disable or retire it only through the host's supported controls.
4. If discovery succeeds but behavior fails, collect the [support bundle](SUPPORT.md) and report a runtime issue rather than a packaging issue.
