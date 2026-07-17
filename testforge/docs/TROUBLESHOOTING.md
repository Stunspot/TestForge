# Troubleshooting

## The stack detector returns `unknown`

Run it from the package or repository boundary that contains the relevant manifest and test configuration. If a monorepo has package-local configs, run detection for that package and preserve the parent impact map separately.

## YAML validation says PyYAML is missing

Use the canonical JSON manifest, or install PyYAML only with explicit approval in the target environment. JSON-compatible YAML eval files remain no-dependency readable.

## A test is marked passed but validation fails

A passed test requires a valid `execution_id` whose record has an integer exit code. Link the captured execution; do not change the test status from memory.

## A referenced test path is missing

Pass the target project root with `--root`. If the artifact is intentionally copy-ready rather than written, mark it `designed` or `unexecuted` and retain the planned destination.

## Result parsing fails

Keep the raw file, mark the execution `unparsed`, and use a generic command record or add a deliberate adapter. Do not infer counts from a truncated log.

## The reviewer rejects a green suite

Inspect the challenged risk, oracle, boundary, and revision. A green suite can be inapplicable, stale, weakly asserted, or incomplete without being technically broken.
