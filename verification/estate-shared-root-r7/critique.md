# TestForge: pending user operations and draft custody

This is a bounded reopening of the accepted 2.0.0 r5 verification practice. The accepted source and native bundle agree. Its concurrency reference already correctly teaches invariants, read/check/write hazards, deterministic interleavings and observable barriers. Its entrypoint already routes asynchronous work into reliability doctrine. Claiming that race testing was absent would be false. The narrower weakness is that the interactive journey lens does not make the user's editable working state part of that operation boundary, and its reviewer lens does not supply a discriminating acceptance criterion for it.

## ASYNC-01 — The journey stops at the command, while its effects remain pending

Evidence: `references/specialized/customer-journeys.md` calls for saved work across refresh, return, routes and recovery, and lists delayed saves among content-shape variations. `concurrency-and-races.md` correctly covers interleavings, but neither connects replacement/read/parse/hash/confirmation/commit to a draft or record identity that can change during the wait. The actual r3 Garagecraft Edge observation says a late import replaced newly edited work; the r3 file records no browser exceptions. Moving m3 started replacement while clean, accepted notes during its delayed sample load, then erased them with zero dialogs. These are real product observations supplied by the estate review, not a fresh model trial or proof TestForge was invoked on those versions.

Impact: a sequential happy-path import and a no-console-errors assertion can both be green while the task loses the work it promised to protect. Merely adding delay or checking the state at invocation cannot discriminate this failure.

Action: route pending user operations from the journey lens into the existing race practice. Trace identity and draft revision through the whole operation, hold the final asynchronous boundary before mutation, then perform an actual conflicting user action. Assert visible and stored post-state and the permission that applies at commit. Let the product choose serialization or preserved editable state with conflict handling; tests must exercise the selected contract rather than mandate a lock.

## ASYNC-02 — Review lacks a concrete wrong-record and stale-completion oracle

Evidence: the reviewer journey file is byte-identical to the operator journey file. The reviewer already challenges concurrency and post-state in general, but has no situated question separating a cancelled request from a cancelled visible dialog, or an editor bound to record A from a callback applied to record B. Family History's captured Edge baseline records an old draft inserted into the newly opened packet, a cancelled import completing anyway, and navigation discarding an unapplied record draft.

Impact: a cancellation status or newly selected title can masquerade as success even though the stale callback still writes later. Testing only the displayed state immediately after cancellation misses the consequential completion.

Action: give the reviewer a compact, self-contained pending-operation evidence lens. Require the trace to cross the invalidated completion, inspect both identities and their drafts, and pair the rejection with useful same-file retry/valid replacement. Reject a readiness claim for these affected outcomes when the critical trace is missing; preserve a truthful narrower claim. Do not expand this into a mandatory browser matrix for every pure function or unrelated release.

## ASYNC-03 — Existing examples do not demonstrate the decisive interleaving

Evidence: current packaged examples cover a Python regression, parser edges and a TypeScript API change. None demonstrates a browser operation held before commit while the user creates newer draft state. Existing concurrency prose gives the right technique but leaves the important boundary selection implicit for this recurring UI mechanism.

Impact: a model or practitioner can reproduce the vocabulary while its test waits only for a final render, disables editing artificially in the test, or uses a mock that removes the actual event boundary. An all-reject implementation could pass only negative cases.

Action: add one situated worked example with an explicit invariant, observable barrier, user action, forbidden effects, matched useful controls, evidence labels and review consequence. Qualify its oracle using actual isolated Edge against intentionally vulnerable and protected synthetic implementations. Keep fixture proof distinct from the product under review and from model adherence. No provider call, model efficacy experiment, real user study or production data is needed for this bounded correction.

## Scope and treatment

Repair the existing verification/reviewer responsibility; do not redesign TestForge, add a validator field, enforce a particular UI architecture, or change activation/stopping/authority/sealing rules. Use Promptcraft for these runtime instructions. Existing customer installation/usage documents and shelf sidecars remain true and unchanged, so no Hesperos reauthoring is claimed. A new pedagogic model reference is runtime instruction/example, not a revised customer installation guide.

This is an in-place edit of 2.0.0: the accepted promise already includes customer outcomes, concurrency, cancellation/recovery, evidence-based oracles and independent challenge. It adds no supported host, interface, execution command, integration or commercial promise. The complete delta from accepted r5 will be recorded and packaged as a private reproducible candidate for root acceptance. Root owns Free integration and all central delivery.

## Corroborating evidence received during repair

Root independently reproduced two additional Home Inventory r1 failures in `product-audits/nova-emergent-home-inventory-builder/root-review-r1/async-probe/counterexamples.json`: a save left fields editable then lost the later correction on response, and an old bootstrap Refresh snapshot erased a newly committed item from the visible catalog while native storage still retained it. The same responsibility extends beyond file replacement: operation lifetime includes form fields, and an old read cannot become current view truth after a successful mutation. This corroborates ASYNC-01/02; it is not a fourth product-specific rule or a new model trial. Root owns those repairs.

## ASYNC-04 — Root follow-up: a current output contract points outside its skill

Independent review resolved all five retained scanner reports. Four are precisely bounded fixture/import/lineage references. The fifth is a real defect: output-contract.md sends the reader two directories upward for a schema actually inside its own assets/schemas. Following the link fails in the portable skill. Root r7 corrects the owned link and retains the schema; contained fresh-package resolution plus native validator checks qualify it. Prior acceptance is not a reason to retain a demonstrated defect.
