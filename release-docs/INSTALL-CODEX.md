# Install TestForge in Codex

Use a Codex build with the native `plugin marketplace` and `plugin add` commands. This path was checked on Codex CLI 0.144.5; plugin support in another build requires that build's own supported controls.

Extract `TestForge-v2.0.0.zip` into a new directory. Open a terminal in its `testforge-v2.0.0/` release root. Python 3.10+ is recommended for the portable verifier; without it use the checksum and reduced-assurance path in the [quick start](QUICK-START.md).

## Install the complete plugin

Run these commands from the extracted release root:

```text
python tools/verify_release.py .
codex plugin marketplace add . --json
codex plugin add testforge@cd-testforge --json
codex plugin list --json
```

Require the verifier to return `"ok": true`. The bundled `.agents/plugins/marketplace.json` registers the existing `cd-testforge` marketplace and points to the complete `codex/testforge/` plugin. The install result should identify `testforge@cd-testforge`, version `2.0.0`, and its actual installed path. Check that the host lists the plugin as enabled. Keep the extracted root available while it is a configured local marketplace.

If the same marketplace is already registered to a different location, inspect that source through the host's plugin manager before changing it. Preserve an older installed copy until its provenance is known; use the host's supported disable/remove controls for duplicates rather than deleting arbitrary cache files.

Open a fresh task after installation. Discover `software-verification` and `verification-reviewer`, then invoke the starter prompt from the [quick start](QUICK-START.md). Package verification, native installation, fresh discovery and useful operation are separate observations. A successful file copy alone proves none of the latter three.

## Recovery and rollback

If static verification fails, preserve the failed result and extract a fresh copy from the canonical ZIP. If the plugin remains absent, check the exact CLI error and selected marketplace root. It must contain `.agents/plugins/marketplace.json` and `codex/testforge/`; selecting the `skills/` child is not this installation path.

If discovery succeeds but behavior fails, collect the [support bundle](SUPPORT.md). Retain the target, invocation and original response so a package defect can be distinguished from an unsupported host or model configuration.

Use Codex's plugin manager to disable or remove TestForge. Start a fresh task and confirm its two handles are no longer discoverable. To roll back, register and install the retained older complete release through the same supported flow, then verify the displayed version and a fresh invocation. Removing TestForge does not delete verification reports or other project files created while using it.
