# Adversarial verification — TestForge

Receipt: `TESTFORGE-ADVERSARIAL-0c93516-ff21cef0-20260812`

- Candidate: `0c935166bc35baafb39108dd888812e64023c0aa`
- Fingerprint: `ff21cef0cb1e7155769a9a4a06688b2b240eb2662c0dc6ca92c1cfb57d71fee7`
- Local candidate disposition: `PASS`
- Public release disposition: `BLOCKED — PUBLICATION NOT EXECUTED`

## Challenges performed

- Re-read customer claims against both skill sources, package manifest, current/frozen release manifests, validators, and tests.
- Challenged current-vs-frozen release identity, host support, portal publication/scanning, activation language, privacy/network behavior, and evidence authority.
- Exercised all local tests and validators after the final content change.
- Verified every local Pages route, fragment, and asset for index and 404.
- Opened all three final visual files and separately challenged role identity, text requirements, crop, hierarchy, contrast, distinctness, and wiring.
- Re-examined responsive CSS after a focus-color change and caught/repaired corrupted mobile grid declarations before the bound commit.
- Queried the live repository, Pages configuration, rendered HTML bytes/markers, live hero bytes, main-branch rule, and repository Open Graph configuration without mutation.

## Remote facts at review time

- Remote `main`: `93120abaa39c26a6f0ec494bdff0c7e6f92344cf`
- Pages: built from `main:/docs` at `https://stunspot.github.io/TestForge/`
- Live index: HTTP 200, 17,593 bytes, but lacks the candidate `start`, `troubleshooting`, `privacy`, and `evidence` sections and lacks the candidate social-card reference
- Live Pages hero: HTTP 200, 1,481,766 bytes — the superseded generic server-room image, not the reviewed 2,212,223-byte candidate
- GitHub repository Open Graph image: unconfigured (`open_graph_image_url` null)
- Main protection: ruleset `20247129`, required status `line-ending-policy`, no observed bypass path

## Blocking decision

A push would trigger four GitHub-hosted test jobs (one line-ending job and a three-OS matrix) plus a Pages deployment. The user has stated that hosted Actions capacity is exhausted and instructed that it not be consumed. Therefore publication is intentionally NOT EXECUTED. The candidate cannot receive a live repository/Pages/assets PASS until capacity or an authorized alternative exists. GitHub repository social-preview upload also remains unexecuted because the supported control is the repository Settings UI and browser/GUI control is explicitly out of scope.

No live PASS is inferred from the existing 200 response. Any governed-file change invalidates this receipt.
