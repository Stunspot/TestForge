# Capability matrix

| Capability | Core package | Requires host/tool | First-release status |
|---|---|---|---|
| Scope, impact, risk, invariant, scenario, release reasoning | Yes | LLM host | Included |
| Independent skeptical review | Yes | separate activation/context | Included |
| Repository inventory and stack detection | Scripts | Python + file access | Included |
| Manifest and traceability validation | Scripts | Python | Included |
| JUnit/Jest/command result normalization | Scripts | Python | Included |
| Test smell heuristics | Scripts | Python + files | Included; not a correctness oracle |
| TypeScript Jest/Vitest authoring | Doctrine | target framework locally available | Included guidance |
| Python pytest/unittest authoring | Doctrine | target framework locally available | Included guidance |
| Local test execution | Coordination | shell + target environment + authorization | Capability-dependent |
| GitHub PR context | Adapter | authorized connector or CLI | Capability-dependent overlay |
| Browser/Playwright, mutation, fault injection, deep CI integration | No | later expansion | Deferred |
| Active penetration testing, compliance certification, formal proof | No | different product/authority | Out of scope |
| Autonomous release authority | No | accountable human | Out of scope |
