# Proof-of-value demo

Give TestForge a payment-webhook retry diff, two existing retry-counter tests, a one-line requirement (“retry failed events three times”), the package manifest, and a failing CI log.

A generic test generator writes more retry tests. TestForge reconstructs the commit points, identifies duplicate fulfillment between event publication and persistence, distinguishes transport retry from business idempotency, recognizes the CI failure as a stale fixture rather than the production defect, and creates:

- a change-impact map;
- a critical duplicate-processing risk and idempotency invariant;
- policy unit tests plus repeated-delivery and crash-window integration scenarios;
- normalized execution evidence and failure triage;
- a `NOT_READY` assessment with the exact remediation required.

The buyer-visible shift is from “AI wrote five tests” to “AI found the release-blocking failure mode, created the evidence needed to reproduce it, and showed why existing green tests were misleading.”
