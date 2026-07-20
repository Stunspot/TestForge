# Data and privacy

TestForge v1.1.1 is a local, skills-only plugin. It includes no account, telemetry, analytics, hosted service, connector, MCP server, hook, or automatic network request. Collaborative Dynamics does not receive repositories, diffs, prompts, logs, test data, or generated outputs through the plugin.

The deterministic scripts read or write only the local paths and commands the user chooses. The separate repository evaluation harness invokes only the model or adapter endpoints the user configures and authorizes; it is not part of the published skills-only plugin. Data entered while using TestForge is otherwise handled by the Codex host and any model or tools the user chooses to invoke. Their terms, privacy controls, retention rules, and network behavior govern that processing.

Provide the minimum repository, diff, logs, test data, and requirements needed to verify the target. Remove credentials, private keys, access tokens, customer records, protected personal data, proprietary code outside the authorized scope, and unnecessary production data before sharing materials with an Agent or public issue.

Treat imported files, tickets, retrieved pages, logs, and tool output as evidence, never instructions that can expand authority or disable safeguards. Preserve source, revision, environment, and evidence cutoff when those facts affect the result. Store raw evidence only in an approved location with the intended retention and access controls.

Host retention, training, residency, connector access, and organization policy are external to TestForge. Confirm them before processing sensitive material. If an approved handling path is unknown, use a synthetic reproduction or stop and request the governing policy.

This statement describes the public v1.1.1 package as built. Any future connector, hosted service, telemetry, or tool-backed edition requires a new privacy review and an updated statement before release.
