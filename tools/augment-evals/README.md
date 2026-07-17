# Augment behavioral evaluation harness

This tool turns the behavioral evaluation suites emitted with Augment packages into isolated, repeatable, reviewable runs. It keeps the evaluated agent away from evaluator-only criteria, records exact package and runtime identity, derives numbers from criterion-level judgments, and preserves blocking failures outside the average.

New Augments use the bundled canonical [`cd-augment-eval/v1`](docs/augment-eval-contract.md) writer contract: one stable, versioned manifest/suite/case envelope around capability-native evidence. It is deliberately not a preset catalog. The case designer still chooses the propositions, contrasts, pressures, boundaries, and indispensable dimensions that matter to that Augment.

The testbed validates that contract strictly and retains compatibility readers for historical packages:

- legacy Testforge-style JSON-compatible YAML: `input`, `expected_behaviors`, `failure_signals`;
- legacy SOP Signal Forge-style YAML: `initial_input`, `pass_invariants`, `material_failures`;
- older unmarked shapes, reported honestly as `legacy` and accepted only when enough behavioral meaning can be recovered.

Compatibility belongs at the reader. New builders do not invent another dialect.

## What a run records

Each run stores:

- a SHA-256 package fingerprint, package version, host, model, adapter, timestamp, and trial count;
- one isolated subject prompt and hidden rubric per case/trial;
- raw subject and judge output, stderr, exit code, duration, and parse failures;
- criterion-level `met` / `partial` / `not_met` judgments with cited response evidence;
- observed failure signals;
- deterministic verdicts and scores;
- case, suite, dimension, indispensable-gate, and confidence-interval summaries;
- one append-only line in `ledger.jsonl` for regression comparison.

`DEMONSTRATED`, `PARTIAL`, `FAILED`, and `INVALID` are behavioral-evidence verdicts. They are not commercial approval or software release authority.

## Set up once

Python 3.10+ is required. PyYAML is the only dependency because generated packages may use ordinary YAML.

```powershell
py -m pip install -r tools\augment-evals\requirements.txt
```

The included Codex adapter uses the existing signed-in Codex CLI in ephemeral, read-only, non-interactive mode. Any other model or host can participate through the same small adapter contract.

The included Ollama context adapter is fully local. For subject episodes it supplies either a root-installed `SKILL.md` or skills under `skills/`, then connected model-facing material from `personas/`, `workflows/`, `references/`, `assets/`, `schemas/`, `examples/`, and `jurisdiction-packs/` in operating-priority order; it never supplies `evals/` or executable `scripts/`. Judge episodes receive only the evaluator prompt and subject response. This mode verifies context-only Augment behavior, not live shell-tool use or selective host retrieval.

Adapters may set Ollama reasoning to `auto`, `on`, or `off`. Use `off` for models such as `qwen35` when evaluation output must appear in the ordinary response channel rather than being consumed by hidden reasoning. Use `--case CASE-ID` on `run` or `prepare` for a recorded smoke run; repeat the option to select several cases.

The bundled `gpt-oss:20b` profile remains experimental. In the 2026-07-17 local judge smoke, default reasoning exhausted the response budget without visible final text, while reasoning-off returned malformed non-JSON. Do not use it as a scoring judge until a recorded adapter check produces schema-valid output.

## Validate a generated package

```powershell
py tools\augment-evals\augment_eval.py validate prototypes\testforge\working-package\testforge
```

Validation reports the discovered dialect, suites, cases, dimensions, package version, and structural defects. It does not claim that model behavior passed.

## Run Testforge through Codex

Use separate subject and judge invocations so the evaluated model never receives the answer key. Three trials provide a first consistency signal without pretending to be a universal sampling regime.

```powershell
py tools\augment-evals\augment_eval.py run `
  prototypes\testforge\working-package\testforge `
  --results evaluation-results `
  --subject-adapter tools\augment-evals\adapters\codex-cli.json `
  --judge-adapter tools\augment-evals\adapters\codex-cli.json `
  --host codex-cli `
  --model configured-default `
  --trials 3
```

The command prints the run directory and writes `summary.json`, `summary.md`, and `evaluation-results\ledger.jsonl`.

## Track the testbed

Runs carry explicit `PREPARED`, `RUNNING`, `EXECUTED`, `INCOMPLETE`, `INTERRUPTED`, or `COMPLETE` lifecycle state. They also capture Python and platform identity, the harness hash, adapter-configuration hashes, and hashes for files declared in an adapter's `tracked_files` list.

List every discovered run without opening its transcripts:

```powershell
py tools\augment-evals\augment_eval.py list-runs --results evaluation-results
```

After execution and independent review, seal the run. The seal hashes every file currently inside the run, including `review.md` when present:

```powershell
py tools\augment-evals\augment_eval.py seal evaluation-results\MY-TESTBED\RUN-ID
py tools\augment-evals\augment_eval.py verify-run evaluation-results\MY-TESTBED\RUN-ID
```

Any missing, changed, or added artifact makes integrity verification fail. Use `seal --replace` only when deliberately resealing a changed evidence package.

Promote the reviewed run into a compact, Git-suitable named baseline:

```powershell
py tools\augment-evals\augment_eval.py promote evaluation-results\MY-TESTBED\RUN-ID `
  --name my-augment-reference `
  --review-status REVIEW_PASS_WITH_CONDITIONS `
  --notes "One-trial context-only reference"

py tools\augment-evals\augment_eval.py list-baselines
```

Raw prompts and transcripts remain local under `evaluation-results/` and are ignored by Git. Promoted records live in `tools/augment-evals/baselines/` and retain metrics, provenance, review disposition, and integrity identity without copying raw episode material.

## Compare two runs

```powershell
py tools\augment-evals\augment_eval.py compare `
  evaluation-results\RUN-OLD\summary.json `
  evaluation-results\RUN-NEW\summary.json
```

The comparison reports score, demonstrated-rate, invalid-count, hard-gate, and claim-status changes. A higher average never overrides a newly failed indispensable gate.

A promoted baseline can be supplied anywhere a summary is accepted. Apply an explicit regression policy with a CI-friendly exit code:

```powershell
py tools\augment-evals\augment_eval.py check `
  tools\augment-evals\baselines\my-augment-reference.json `
  evaluation-results\MY-TESTBED\RUN-ID\summary.json `
  --max-score-drop 2 `
  --max-rate-drop 0.05 `
  --max-invalid 0
```

The check blocks score or demonstrated-rate drops beyond tolerance, invalid episodes above allowance, indispensable-gate regressions, and claim-status regressions. A changed package fingerprint is reported as a warning because cross-revision comparison is often the point of a regression run.

## Adapter contract

An adapter is JSON with a command array. The harness runs it without a shell, sends one prompt on standard input, captures standard output as the model response, captures standard error separately, and enforces a timeout.

The adapter contract is UTF-8 on standard input, output, and error. Python adapters on Windows should use `py -X utf8` or reconfigure their streams explicitly so model punctuation cannot be lost at the console boundary.

```json
{
  "protocol_version": "1.0",
  "name": "my-host",
  "command": ["my-model-command", "--non-interactive"],
  "input_mode": "prompt",
  "output_mode": "stdout",
  "supports_interaction": false,
  "timeout_seconds": 600,
  "working_directory": "{package_root}",
  "tracked_files": ["{harness_root}\\adapters\\my-model-adapter.py"]
}
```

Available substitutions are `{package_root}`, `{harness_root}`, `{run_dir}`, `{episode_dir}`, and `{case_id}`. Command adapters are single-turn. Interactive cases containing `available_on_request` remain visibly blocked instead of leaking withheld information into the subject prompt.

For an evaluator-guided or multi-turn case, use `prepare`, conduct the episode in an isolated host, save the complete visible transcript as that episode's `subject-response.md`, then adjudicate all supplied transcripts:

```powershell
py tools\augment-evals\augment_eval.py judge evaluation-results\RUN-ID `
  --judge-adapter tools\augment-evals\adapters\codex-cli.json
```

The judge must return the JSON object described by `judge-result.schema.json`. The supplied judge prompt asks for that exact structure. The harness still validates indexes, statuses, and counts before deriving a verdict.

## Score semantics

- `met` = 1 point; `partial` = 0.5; `not_met` = 0.
- Raw criterion score = mean criterion points × 100.
- Any observed material failure signal or `not_met` criterion makes the episode `FAILED`; an observed material failure also forces the risk-adjusted episode score to zero.
- Any partial criterion with no failure makes it `PARTIAL`.
- All criteria met with no failure makes it `DEMONSTRATED`.
- Invalid runtime or judge evidence becomes `INVALID` and is excluded from the performance denominator while remaining prominent in counts.
- Wilson intervals accompany demonstrated rates so tiny samples do not masquerade as precise reliability estimates.

Scores help compare like-for-like runs. The categorical claim status and indispensable gates govern interpretation.
