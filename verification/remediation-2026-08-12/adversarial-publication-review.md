# Final adversarial publication review — TestForge

Receipt: `TESTFORGE-ADVERSARIAL-PUBLICATION-0c93516-ff21cef0-20260812`

- Governed content: `0c935166bc35baafb39108dd888812e64023c0aa`
- Fingerprint: `ff21cef0cb1e7155769a9a4a06688b2b240eb2662c0dc6ca92c1cfb57d71fee7`
- Starting state: `UNKNOWN`
- Disposition before publication: `READY_WITH_RESIDUAL_RISK`

## Decision-changing corrections

1. The prior blocker generalized exhausted private-repository Actions allowance to this public repository. Official GitHub billing documentation states standard hosted runners are free in public repositories; successful public runs in this remediation establish availability.
2. The prior job count covered only a direct main push. Protected publication through a feature branch and PR expands to 13 jobs: 4 branch, 4 PR, 4 main, and 1 Pages deployment. All are public standard-runner jobs with zero billable minutes; no retry is planned.
3. Repository Open Graph configuration is not null now. GitHub GraphQL returns a live image whose downloaded 600,421 bytes exactly equal `assets/testforge-social-preview.png`, SHA-256 `9eb81f699f7b8bfdfa4b6ec41cee2883563d1d8de79bed2298167b90c212ec12`.

## Fresh adversarial evidence

- Repository tests: 23 of 23 PASS.
- Packaged tests: 11 of 11 PASS.
- Augment-evals harness: 46 of 46 PASS.
- Package verifier: 226 files, zero errors or warnings.
- Eval-suite validator: 10 cases, 11 dimensions, PASS.
- Release manifests and source parity: PASS.
- Frozen v1.1.5 verifier: 2 Claude archives, 130 files, 100 source files, 3 ZIP containers, 228 ZIP members, zero findings.
- Actual pixels reopened for README hero, Pages hero, and social card; all three roles remain distinct and suitable, and the social card visibly says `TESTFORGE` and `SOFTWARE VERIFICATION THAT ARGUES BACK.`

## Remaining release conditions

- Exact PR head receives all eight branch/PR check results and required `line-ending-policy` succeeds.
- Protected merge completes without ruleset weakening.
- Main checks and Pages deployment succeed for the final merge commit.
- Live README, Pages HTML, custom 404, links, metadata, three image assets, and repository Open Graph bytes match the reviewed candidate.
- GUI-rendered browser behavior and assistive-technology behavior remain `NOT TESTED`; no claim is made otherwise.

Any governed-file change invalidates this review.
