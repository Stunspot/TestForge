# TestForge: host and evidence boundary

## Claim ladder

1. **Packaged:** manifests, hashes, ZIP safety, and documentation pass static checks.
2. **Installed:** the host reports a completed plugin or Skill import.
3. **Discoverable:** a fresh task or chat lists the expected handle.
4. **Invoked:** an explicit probe reaches the intended capability.
5. **Healthy:** required tools and dependencies operate on representative work.
6. **Published:** the approved repository or directory exposes the intended release.
7. **Valuable:** a customer completes the promised job successfully.

Evidence at one rung does not prove the next. Use [validation](VALIDATION.md) for the package rung, the [installation guides](INSTALL-CODEX.md) for Codex or [Claude](INSTALL-CLAUDE.md) for the host rungs, and [support](SUPPORT.md) when the observed rung is lower than expected.

## Model and judgment boundary

A working package does not qualify every model for release judgment. Evaluate the actual model, context route, tools and review arrangement with task-specific positive and adversarial controls. A local context-only smoke can expose contradictory verdicts or weak controls; it cannot establish live tool use, broad reliability or independent review. Preserve failed probes and configuration limits. If a model cannot keep candidate evidence, control evidence and final status consistent, use a qualified host or independent reviewer instead of treating that configuration as a release oracle.
