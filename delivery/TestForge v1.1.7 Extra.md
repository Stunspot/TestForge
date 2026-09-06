# Description

TestForge is a free two-SKILL verification system for frozen release candidates. `software-verification` reconstructs impact, ranks consequential failure risks, builds meaningful oracles, runs only checks that can change the bounded verdict, and returns a traceable release assessment. `verification-reviewer` then attacks that evidence chain for omissions, weak tests, unsupported claims, and conclusions that outrun the proof. Together they turn verification into a quality ratchet instead of an ornamental pile of green checkmarks.

# Usage Notes

Copy the .zip from "Additional Files" to your Codex, Claude Code, or other harness (or add the .zip file to a knowledge base of a project on Chat) and install the contained TestForge Augment Agent SKILLs. The prompt this post contains has a clean install and onboarding process but is not required. Hit copy to clipboard and paste to your harness in chat with the .zip file.

- Give `$software-verification` a completed, frozen candidate and an explicit release-readiness claim. Ordinary implementation work does not need the full TestForge apparatus.
- Keep the builder and verifier roles distinct. A discovered product defect or newly exposed requirement returns to builder custody.
- Use `$verification-reviewer` on the finished evidence package, preferably in a fresh context.
- Every check, retry, artifact, and reviewer pass should be capable of changing the bounded verdict. TestForge does not certify defect freedom or authorize release.

Public GitHub Repo: [TestForge](https://github.com/Stunspot/TestForge)

Project Site: [TestForge verification workbench](https://stunspot.github.io/TestForge/)

# Changelog

v1.1.7 - Tightened activation to explicit frozen-candidate release verification, enforced decision-changing evidence, and added bounded recovery and stopping rules.
v1.1.6 - Added metered-verification safeguards for quota-limited environments.

# Tags

software verification, release readiness, risk-based testing, adversarial review, evidence, regression gates, behavioral evals, quality assurance, Codex, Claude, Agent SKILL, Augment
