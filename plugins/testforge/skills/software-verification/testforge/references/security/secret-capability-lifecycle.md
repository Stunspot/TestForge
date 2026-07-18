# Verify a secret capability as a state machine

Use this pattern when one operation mints a secret capability, an out-of-band channel delivers it, and a later operation redeems it. Password-reset links, magic links, invitations, enrollment tokens, and one-time recovery codes share this shape.

Keep issuance and redemption separate. The public request response must not expose eligibility or the secret. Observe the secret only through an authorized fake delivery sink. Use the real persistence boundary for claims about active, consumed, expired, or revoked state.

## State model

`absent -> active(until deadline) -> consumed | expired | revoked`

A second issuance request needs contract authority: it may invalidate the prior capability or permit a bounded number of active capabilities. Preserve that question if unspecified; always test the authorized active-count invariant and prior-capability disposition.

## Minimum oracle matrix

| Scenario | Required observations |
| --- | --- |
| Eligible versus ineligible request | Same public status, body shape, headers, and material timing class; protected account state unchanged; no public secret or eligibility signal |
| Issuance and delivery | Authorized fake sink receives the intended secret; public response and logs contain no secret; persistent active-capability count and deadline match policy |
| Repeated issuance before use | Active-capability count remains within policy; prior capability is still active or invalidated exactly as the contract requires; each accepted issuance produces exactly its authorized delivery, with no extra duplicate delivery or event |
| Fresh valid redemption | Only the intended account state changes; capability atomically becomes consumed; required audit or event occurs once |
| Immediate reuse | Denial; protected state unchanged; no downstream effect; consumed state remains consumed |
| Unused expiry | Start with a fresh unconsumed capability, advance an injected clock beyond the deadline, then assert denial, unchanged protected state, no downstream effect, and persisted expired or unusable state |
| Concurrent redemption | Competing uses produce at most one successful protected-state change and one required downstream effect |

Do not use a consumed capability to prove expiry; consumption may mask the expiry defect. Do not mock the token store while claiming persistent single-use or atomicity evidence. A unit test may establish local policy, but API plus real persistence is the credible layer for lifecycle and authorization semantics.
