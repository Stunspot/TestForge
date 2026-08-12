# TestForge v1.1.6

## What changed

TestForge now treats finite verification capacity as part of the test plan, not as an invisible environmental detail. Before it recommends or invokes hosted CI, device or browser farms, paid cloud checks, or another quota-limited route, it requires a fresh capacity observation for the exact billing scope and calculates the complete planned run.

The estimate includes duplicate triggers, matrix fan-out, retries, runner ceilings, and current provider billing multipliers while preserving a human-set reserve. Unknown, stale, post-refresh, insufficient, provider-refused, reserve-consuming, or unauthorized paid execution produces a hold without launching a job merely to discover capacity.

The new deterministic assessor records the included-capacity decision and rejects caller-supplied claims of paid authority. It never permits paid dispatch. A separate trusted dispatcher would have to resolve and consume principal-controlled authority bound to an exact execution, plan digest, billing scope, expiry, and maximum paid minutes; that mechanism is not included in TestForge.

## Documentation

Quick-start, recurring workflow, capability, limitation, host, provenance, and maintainer guidance now explain the metered-verification safeguard and the evidence it requires. A packaged JSON schema and worked plan template define the assessor input; a five-field response template locks snapshot fidelity, reserve-aware arithmetic, substitute disclosure, and bounded authority requests.

## Evidence boundary

The package includes deterministic unit coverage for capacity states, refresh boundaries, matrix and retry expansion, billing multipliers, retained reserve, exact billing scope, and rejection of self-asserted paid authority. Static package and local execution evidence do not prove live provider-meter accuracy, hosted-run success, customer installation, or defect freedom.
