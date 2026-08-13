# Install TestForge in Claude

Claude capabilities, eligible plans, organization controls, and interface labels can change. Check the current official Claude Skills guidance before installation. The package provides two independent upload archives; it cannot enable host or organization capabilities.

1. Confirm the account or organization exposes custom Skills and any execution capability needed for deterministic scripts.
2. Follow the current host workflow for uploading a custom skill.
3. Upload `claude-ai/software-verification-v1.1.7.zip` and `claude-ai/verification-reviewer-v1.1.7.zip` separately.
4. Enable both skills if the host provides an enablement control.
5. Start a new conversation and test the operator and reviewer separately.

Do not combine the archives, upload the entire repository, or upload a ZIP containing only `SKILL.md`. Each supplied ZIP contains one matching top-level skill folder and its runtime dependency closure.

Live upload, enablement, discovery, progressive resource loading, script execution, reviewer handoff, and persistence were not exercised for this release. If a skill does not appear, preserve the visible error and check account capabilities, organization policy, upload state, and enablement before changing the archive.
## Update

Record the installed package version and preserve any local evidence you need. Remove or disable both existing TestForge skills through the current host interface, upload both same-version replacement archives separately, enable them if required, then start a new conversation and repeat the operator and reviewer probes. Do not update only one skill.

## Remove and clean up

Remove or disable both TestForge skills through the host's current skill-management interface and begin a new conversation to confirm neither is discoverable. Delete downloaded ZIPs if local retention is unnecessary.

TestForge itself has no account, hosted store, telemetry database, or background service. Host conversations, uploaded skill copies, generated files, and model-provider records are controlled by the host and organization, not by TestForge; use their retention and deletion controls. Locally retained manifests, reports, raw evidence, tests, and evaluation runs remain ordinary files and must be reviewed under the project's data policy.
