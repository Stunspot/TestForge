# Adversarial verification — TestForge

Receipt: `TESTFORGE-ADVERSARIAL-441a22b-af19aa44-20260812`

- Candidate: `441a22b8ac1f6fda9c4d7ba355f5cca19f365d1c`
- Fingerprint: `af19aa440e63bfd1d4fd8e4d9e6c516dabf03892747743b1de138600e191c7b3`
- Local candidate disposition: `REVIEW_PASS`
- Publication disposition: `READY_TO_PUBLISH`; live exact-content oracles remain mandatory

## Challenges performed

- Re-read every declared customer document and attacked current-vs-historical release identity, supported hosts, activation language, privacy/network claims, portal state, release authority, cleanup, support, and licensing against actual package sources and tests.
- Reconciled remediation content with newer v1.1.6 main rather than overwriting the release: current package, frozen archive, retained v1.1.4 portal packet, workflows, documentation, and evidence now stay distinct.
- Found and repaired the stale v1.1.5 current-authority pointer, ambiguous historical Build Week counts, and two unstable directional references. The verbatim MIT clause was preserved.
- Challenged documentation structure separately from substance: 49-document full read, Hesperos lint, local-link tests, 22 external URLs, and current-release checks all pass.
- Reopened all three images and challenged role distinction, identity, crop safety, hierarchy, contrast, artifacts, required social text, and wiring. All pass.
- Challenged the merged product claims through 98 unit/harness tests, 233-file package verification, 12-case eval validation, current manifests, frozen v1.1.6 verification, and line-ending checks. All pass.
- Corrected the prior false Actions blocker: this is a public repository and standard hosted runners are free; the complete 13-job remediation graph has zero billable minutes.

## Remaining publication oracles

- PR checks pass on the synchronized exact head and protected merge completes without ruleset weakening.
- Main checks and Pages deployment pass for the final merge commit.
- Live raw README, Pages HTML/CSS/404, navigation/fragments, assets, metadata, and repository Open Graph bytes equal the reviewed candidate.
- GUI-rendered browser and assistive-technology behavior remain `NOT TESTED`; no later receipt may promote them without direct execution.

Any governed-file change invalidates this review.
