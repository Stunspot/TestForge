# Install TestForge in Claude

Claude capabilities, eligible plans, organization controls, and interface labels can change. Check the current official Claude Skills guidance before installation. The package provides two independent upload archives; it cannot enable host or organization capabilities.

1. Confirm the account or organization exposes custom Skills and any execution capability needed for deterministic scripts.
2. Follow the current host workflow for uploading a custom skill.
3. Upload `claude-ai/software-verification-v1.1.0.zip` and `claude-ai/verification-reviewer-v1.1.0.zip` separately.
4. Enable both skills if the host provides an enablement control.
5. Start a new conversation and test the operator and reviewer separately.

Do not combine the archives, upload the entire repository, or upload a ZIP containing only `SKILL.md`. Each supplied ZIP contains one matching top-level skill folder and its runtime dependency closure.

Live upload, enablement, discovery, progressive resource loading, script execution, reviewer handoff, and persistence were not exercised for this release. If a skill does not appear, preserve the visible error and check account capabilities, organization policy, upload state, and enablement before changing the archive.
