# TestForge v1.1.0 release notes

Release date: 2026-07-18

TestForge v1.1.0 is the self-contained dual-host release. It keeps TestForge free, open, and public while making both constituent skills directly installable in Codex, Claude.ai, and Claude Code.

## Changed

- Closed the operator's and reviewer's runtime dependencies beneath their own skill roots.
- Added separate portable Claude.ai upload archives for the operator and reviewer.
- Added current Codex, Claude.ai, and Claude Code installation and recovery guidance.
- Shortened discovery descriptions to the current Claude metadata limit.
- Made independent-review routing explicit and preserved the exact lost guarantee when the reviewer is unavailable.

## Verified

- Current Augment Builder Codex and Claude profiles pass for both folders and both Claude ZIPs.
- Source, archive, and extracted skill contents match byte-for-byte.
- TestForge deterministic tests and package verification pass.
- Canonical evaluation envelopes validate.

## Not established

This release does not establish defect freedom, broad behavioral reliability, live Claude.ai or Claude Code behavior, compliance certification, formal proof, production authorization, or field fitness. The accountable human retains consequential edit, execution, release, and publication authority.
