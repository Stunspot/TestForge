# Public publication preflight

GitHub's official billing documentation observed 2026-08-12 states that standard GitHub-hosted runners are free in public repositories. TestForge is public. Existing workflow expansion is intentionally preserved:

- feature-branch push: one line-ending job plus a three-OS test matrix = 4 jobs;
- pull request: the same 4 jobs;
- merge to `main`: the same 4 jobs plus one Pages deployment = 5 jobs;
- total: 13 public standard-runner jobs, zero automatic retries planned, zero billable minutes, no private allowance or paid capacity.

Conservative raw ceiling: `13 jobs × 360 minutes × 0 billable multiplier = 0 billed minutes`. The required `line-ending-policy` remains enforced by ruleset 20247129; no ruleset change or bypass is required.

Official sources:
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
