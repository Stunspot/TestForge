# Public publication preflight — TestForge

Official GitHub billing documentation observed 2026-08-12 states standard GitHub-hosted runners are free in public repositories. TestForge is public; private-repository allowance exhaustion is not this repository’s billing boundary.

Observed and remaining execution graph:

- completed earlier feature-branch run under the pre-v1.1.6 workflow: 4 public standard-runner jobs, all passed;
- branch synchronization after v1.1.6 reconciliation: the new workflow has no feature-branch `push` trigger; the open pull request can create 4 PR jobs;
- merge to `main`: 4 test jobs plus 1 Pages deployment;
- complete remediation maximum: 13 public standard-runner jobs, zero automatic retries planned, zero billable minutes.

Conservative raw ceiling across the 13-job graph: `13 × 360 = 4,680 raw runner-minutes`; public standard runners are free, so billed minutes are zero. Ruleset `20247129` still requires `line-ending-policy`; no bypass or ruleset weakening is required.

Official sources:
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
