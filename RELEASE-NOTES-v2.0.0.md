# TestForge v2.0.0

TestForge 2.0.0 gives the accepted maintained verification behavior a new release identity. Both separately packaged skills, `software-verification` and `verification-reviewer`, ship in the 2.0.0 distribution family.

## Compatibility and migration

The metered-verification assessor no longer emits the JSON field `plan_sha256`. The originally shipped v1.1.7 customer archive contained that field even though a later canonical-source repair had already removed it. External callers may depend on the shipped output, so this release uses a conservative major version boundary rather than claiming backward compatibility.

Update callers that require `plan_sha256` to consume the decision fields without that property. A trusted dispatcher that authorizes paid execution must bind its authority to the exact execution and complete canonical plan content, as described in the metered-verification guide; the assessor never grants paid dispatch or creates a custody receipt. Existing capacity arithmetic, reserve rules, hold outcomes, and authority boundaries remain in force.

## Instruction disclosure

The operator now reaches mandatory metered-verification detail through its existing conditional reference before quota-limited work. The capacity observation, full usage plan, reserve, authorization, and required response-template contract remain mandatory. Local verification loads less irrelevant detail.

The accepted final-seal discipline also defers manifests, archive creation, checksums, and receipts until a stable verdict and review. This release introduces no further runtime redesign.

## Historical custody and evidence

The original v1.1.7 release assets are restored from verified pre-maintenance backups, and its tag remains unchanged. Version 2.0.0 uses its own source tag, packages, archives, and delivery sidecars.

Existing package, tooling, line-ending, documentation, and archive-parity checks establish the recorded static results. Earlier behavioral and installed-host observations remain attached to their original bytes. This release makes no new installed-host or customer-outcome claim.
