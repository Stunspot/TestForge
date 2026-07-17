# Supported environments

## Core operation

Any LLM host that can load Markdown skill instructions and preserve package-relative resources can use the operator and reviewer. Hosts without skill loading can use the fileless fallback.

## Deterministic tools

- Python 3.10 or newer.
- Standard library only for JSON manifests, inspection, diff classification, command capture, JUnit/Jest normalization, smell scans, report assembly, package verification, and eval-structure validation.
- Optional PyYAML only for human-authored YAML that is not JSON-compatible.

## Target stacks

- TypeScript/JavaScript: Jest and Vitest recognition and authoring guidance; npm, pnpm, and Yarn detection.
- Python: pytest and unittest recognition; pip/requirements, Poetry, and uv signals.
- Other stacks: generic risk, scenario, oracle, and command-planning mode without false framework claims.

Windows, macOS, and Linux are supported to the extent Python and the target repository's own tools work there. Target environment setup remains outside the package.
