# TestForge release notes

The current package release is **v1.1.7**. See [RELEASE-NOTES-v1.1.7.md](RELEASE-NOTES-v1.1.7.md) for the completion-governor change and exact evidence boundary.

## Current release

Version 1.1.7 makes TestForge an explicit release-grade assessment of a frozen candidate, not the default tail of implementation. Every check, artifact, retry, reviewer pass, and receipt must be capable of changing the bounded verdict.

A product defect or newly exposed requirement still ends the submitted candidate cycle and returns repair to builder custody. A test, tooling, or environment failure now receives at most one materially different low-cost correction or fallback. If that path fails or encounters another support-layer failure, TestForge classifies the lost guarantee and exits instead of turning verification infrastructure into a new project.

The v1.1.6 metered-verification safeguards remain in force. Unknown or unavailable hosted capacity produces a hold and a bounded substitute; it does not authorize a probe job or reinterpret provider refusal as a product defect.

The maintained repository includes synchronized v1.1.7 package and plugin source plus current Claude upload archives. Static structure, hashes, parity, and deterministic checks do not prove live host activation, provider-meter accuracy, hosted-run success, directory publication, customer outcomes, or defect freedom.

## Historical notes

Version-specific records remain available as RELEASE-NOTES-v*.md. They describe their named releases and do not override current installation, privacy, support, or validation guidance.
