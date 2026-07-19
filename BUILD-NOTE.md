# TestForge v1.1.0 maintenance build note

## Result

The public TestForge repository remains free, open, and dual-host. Its canonical package, Codex plugin, standalone skill folders, Claude upload archives, evaluation testbed, and customer documentation are synchronized to the current Builder and Hesperos standard.

## Documentation

The declared 16-file customer corpus covers orientation, plugin and standalone installation, Codex and Claude paths, first verification, recurring workflows, independent review, behavioral baseline maintenance, recovery, privacy, security, validation limits, support, release history, and provenance. The strict readiness gate applies only to fingerprint `b13863cf1a728c83ae649d2482c3ebf992005b1e5d919ec634b05e08216130a4`.

## Verification

- Current Builder bundle profile passes the canonical package.
- Current Codex and Claude profiles pass both canonical skill folders; Claude profiles pass both upload ZIPs.
- Current Codex profiles pass both plugin skill folders, and distribution tests confirm byte parity with canonical skills.
- All 16 declared customer Markdown files pass Hesperos structural lint.
- A fresh exact-content Hesperos review returned zero material findings and `REVIEW_PASS_WITH_CONDITIONS`; its exact request, response, and input custody are retained.
- Eleven TestForge tool and host-packaging tests, 46 evaluation-testbed tests, and five public-distribution tests pass.
- Canonical package verification and the ten-case evaluation envelope pass.
- The stale CI command targeting a nonexistent nested plugin package was removed; CI now validates the real canonical package and release manifests.
- Two consecutive deterministic rebuilds produced the same Claude archives.
- Claude ZIP SHA-256 values are `126889cb85278d80dd9cc12d3c2dcef072511cb45e6f851de71896fc66ab8cfa` and `d7f9ec1faa9fbe38a8c595cdbb8a01ad1de084a1e2b403f60a66b7016aaadcd2`.
- Canonical and public-repository manifests, archive topology, and source parity validate.

## Exact untested boundary

Fresh standalone Codex activation, live Claude upload and activation, current Claude interface verification, live resource loading, script execution under customer permissions, clean installation, representative first-success behavior, broad repeated-model behavior, representative developer testing, browser, keyboard, screen-reader, and localization testing, accessibility conformance, legal, security, and compliance review, accountable release approval, and production or customer outcomes remain unexecuted.
