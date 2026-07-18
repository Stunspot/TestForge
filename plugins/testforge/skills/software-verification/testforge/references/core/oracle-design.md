# An oracle makes wrong behavior observable

A test is evidence only when its observations discriminate the intended behavior from a plausible dangerous implementation.

Strong oracles usually combine:

- returned value or response contract;
- persistent post-state;
- emitted event or external effect;
- forbidden side effect;
- ordering or timing bound where material;
- invariants preserved across the operation.

Weak proxies include truthiness, “did not throw,” status code alone, snapshot bulk, mock call count without state, or implementation-private details. Strengthen them by naming the user- or system-visible consequence.

For each scenario, ask:

1. Which incorrect implementation should this catch?
2. What observation differs between correct and incorrect behavior?
3. Could a mock, fixture, or assertion make both look the same?
4. What must remain unchanged on denial or failure?

When expected behavior is disputed, preserve competing oracles and seek the domain authority; do not choose the easiest assertion.

Split compound workflows into their actual operations and lifecycle states before drafting tests. A request that creates a later-use capability is not the same operation as consuming it. Compare public responses across meaningful input classes, then separately prove issuance, pre-use state, first use, reuse, expiry, concurrency, persistent post-state, downstream effects, and secret exposure. Control time through an injected clock. An in-memory fake may prove local policy wiring; it cannot establish persistent single-use, atomic consumption, or cross-request behavior.

Use independent controls when one terminal state could mask another: prove expiry with an unused capability beyond its deadline, and prove single-use with a fresh capability immediately after successful consumption. Observe duplicate active capabilities and secret-bearing delivery through an authorized test sink or seam rather than assuming a production response exposes the secret.
