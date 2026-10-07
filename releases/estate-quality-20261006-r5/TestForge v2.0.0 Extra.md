# Description

TestForge is a free two-SKILL verification system for frozen release candidates. `software-verification` reconstructs impact, ranks consequential failure risks, builds meaningful oracles, runs only checks that can change the bounded verdict, and returns a traceable release assessment. `verification-reviewer` then attacks that evidence chain for omissions, weak tests, unsupported claims, and conclusions that outrun the proof. Together they turn verification into a quality ratchet instead of an ornamental pile of green checkmarks.

# Usage Notes

Copy the .zip from "Additional Files" to your Codex, Claude Code, or other harness, or add the .zip to a project knowledge base in Chat. Attach or reference the .zip in chat and say, "Install this Augment." The prompt in this post is optional.

- Give `$software-verification` a completed, frozen candidate and an explicit release-readiness claim. Ordinary implementation work does not need the full TestForge apparatus.
- Keep the builder and verifier roles distinct. A discovered product defect or newly exposed requirement returns to builder custody.
- Use `$verification-reviewer` on the finished evidence package, preferably in a fresh context.
- Every check, retry, artifact, and reviewer pass should be capable of changing the bounded verdict. TestForge does not certify defect freedom or authorize release.

Public GitHub Repo: [TestForge](https://github.com/Stunspot/TestForge)

Project Site: [TestForge verification workbench](https://stunspot.github.io/TestForge/)

# Changelog

v2.0.0 - Maintenance (2026-10-06): Corrects false passes from incomplete test output, rejects contradictory ready verdicts and broken evidence chains, and verifies actual entry, discovery, task completion and resumption for information products. Package builders now preflight portable extraction paths. Further maintenance binds verdicts to current evidence and reviewer conditions, distinguishes real observations from command execution, preserves failed support-attempt history and report caveats, and rejects linked source roots and conflicting archive paths. The maintenance repair also binds the one permitted support correction to explicit test identities. Unrelated success can no longer supersede a failed check; changed interpreter commands remain valid when the same check is actually rerun.

v2.0.0 - Local praxis maintenance (2026-09-12): Added cold-read review that examines complete evidence before author ratings, plus agent/research-harness checks for stale attempts, expired workers, producer identity, malformed review results and truthful completion. Existing frozen-candidate and stopping boundaries remain unchanged.

v2.0.0 - Kept hosted-verification safeguards in their conditional guide; declared removal of the assessor plan_sha256 output field as a compatibility break. Callers must stop requiring that field. Original v1.1.7 assets are restored and its tag preserved.

v1.1.7 - Tightened activation to explicit frozen-candidate release verification, enforced decision-changing evidence, and added bounded recovery and stopping rules.
v1.1.6 - Added metered-verification safeguards for quota-limited environments.

# Tags

software verification, release readiness, risk-based testing, adversarial review, evidence, regression gates, behavioral evals, quality assurance, Codex, Claude, Agent SKILL, Augment

