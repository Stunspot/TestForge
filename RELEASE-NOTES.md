# TestForge release notes

The current package release is **v1.1.6**. See [RELEASE-NOTES-v1.1.6.md](RELEASE-NOTES-v1.1.6.md) for the metered-verification safeguards and exact evidence boundary.

## Current release boundary

Version 1.1.6 treats finite verification capacity as part of the test plan. Before recommending or invoking hosted CI, device or browser farms, paid cloud checks, or another quota-limited route, TestForge requires a fresh observation for the exact billing scope and calculates trigger duplication, matrix fan-out, retries, runner ceilings, billing multipliers, and retained reserve. Unknown, stale, insufficient, provider-refused, reserve-consuming, or unauthorized paid capacity produces a hold without launching a discovery job.

The v1.1.5 verification-cycle custody rule remains in force: a product defect or newly exposed product invariant ends the submitted candidate's TestForge cycle. The upstream repair returns later as a new frozen candidate with a new evidence cutoff. Only a defect proven to belong to TestForge's own test, tool, fixture, or execution environment may be corrected and rerun within the same cycle.

The maintained repository includes synchronized v1.1.6 package and plugin source plus current Claude upload archives. Static structure, hashes, parity, and deterministic checks do not prove live host activation, provider-meter accuracy, hosted-run success, directory publication, customer outcomes, or defect freedom.

## Historical notes

Version-specific records remain available as `RELEASE-NOTES-v*.md`. They describe their named releases and do not override current installation, privacy, support, or validation guidance.