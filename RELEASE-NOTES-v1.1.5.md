# TestForge v1.1.5

## What changed

This patch release restores the verification custody boundary after an unexpected result. TestForge must first classify the cause. A product defect or missing product invariant ends the current verification cycle and returns the candidate upstream as not ready or insufficiently evidenced. TestForge does not patch the product, continue through product failures, or rerun the repaired product inside the same cycle.

A repaired product is a new frozen candidate with a new evidence cutoff and a new verification cycle. Only defects proven to belong to the test, tool, fixture, or execution environment may be corrected and rerun within the existing cycle.

## Package boundary

The release contains synchronized Codex plugin and Claude skill distributions. Static package verification does not prove live host activation, customer outcomes, or defect freedom.
