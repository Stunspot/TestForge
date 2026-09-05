# TestForge

Install and onboard the attached **TestForge v1.1.7** Augment on the current AI harness.

The attached ZIP is the supplied customer package. Inspect the archive and its README, QUICK-START, installation guidance, adapters, archive-custody notes, release notes, and package verifier before changing files. The user authorizes installation of this Augment on the current harness only. TestForge contains two coordinated Agent SKILLs: `software-verification` and `verification-reviewer`. Choose the package's documented Codex plugin, standalone skill, Claude, local-shell, or copy-paste path for this host. Keep the two skills and their referenced resources together. Do not install repository tooling, frozen evidence, evaluation results, or maintainer cargo as runtime content unless the documented host path requires it.

Before writing, detect any existing TestForge installation, its location and version, and the applicable install root. Never overwrite, merge, delete, or replace an existing installation unless the package supplies a documented update path and a recoverable rollback is established; otherwise stop and report the collision. If this host supports durable installation, perform the documented installation and any safe required reload. If it cannot install attached Augments, say so plainly and use the packaged fallback or give the exact manual installation path. Do not improvise a different package layout.

Afterward, report these states separately: pre-existing installation and collision result; package integrity when the verifier or checksum is available; installed locations for both skills; rollback or recovery path; host discovery; one explicit invocation of each skill; relevant tool health; and anything not tested. A visible folder is not proof that either skill is active.

Then onboard me:

1. Explain in no more than three sentences that TestForge verifies a frozen release candidate with risk-ranked, decision-changing evidence and independently challenges whether the resulting verdict is supported.
2. State its boundary: TestForge does not prove defect freedom, certify compliance, authorize production access, or replace accountable release judgment.
3. Ask for the frozen candidate, intended release claim, impact surface, constraints, available evidence, and the decision the verdict must support.
4. Offer this first request: "$software-verification Verify this completed frozen candidate for release. Reconstruct what could break, run only decision-changing authorized checks, and give me one evidence-backed assessment."
5. Explain that `$verification-reviewer` should receive the completed evidence package in a fresh context when practical.
6. Begin only when I provide the candidate and boundary. Keep implementation and verification custody distinct; if verification exposes a product defect or new requirement, return it to builder custody rather than silently repairing the candidate.
