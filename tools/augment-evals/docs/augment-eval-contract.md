# CD Augment Eval v1 — Stable Envelope, Bespoke Evidence

Compose each Augment's behavioral evaluations around the capability's real uncertainty, then serialize them through one predictable interchange shape.

`cd-augment-eval/v1` standardizes **where evaluation meaning lives**. It does not standardize what competence means. The case content remains native to the Augment; the envelope makes that content isolatable, executable, judgeable, comparable across revisions, and legible to the shared testbed.

## Design the evidence before filling fields

Recover the behavioral proposition and the build decision it informs. Choose the smallest cases that expose transfer, consequential discrimination, realistic pressure, authority boundaries, recovery, or another uncertainty earned by the capability.

Use invariance, discrimination, pressure, and boundary cases as design lenses—not a preset menu. Let one sharp minimal pair outperform a decorative catalog. Keep dimensions capability-native. Shared field names enable infrastructure; they do not make unlike competencies numerically comparable.

Keep every top-level case isolated from the others. When competence requires dialogue, withheld evidence, revision, or handoff, model that complete multi-turn episode inside one case with `available_on_request` and evaluate it through the testbed's prepared/evaluator-guided path. This prevents case order from teaching the answer.

## Write JSON-compatible YAML

Write `.yaml` files using JSON-compatible syntax: quoted keys and strings, arrays, objects, booleans, numbers, and `null` only. This remains valid YAML while avoiding implicit dates, booleans, tags, anchors, and parser-dependent scalar behavior.

Every new Augment carries one mandatory `evals/eval-manifest.yaml` and one or more named suite files directly inside `evals/`.

### `eval-manifest.yaml`

```json
{
  "format": "cd-augment-eval/v1",
  "package_version": "1.0.0",
  "episode_mode": "isolated",
  "files": ["core-transfer-cases.yaml"],
  "indispensable_dimensions": ["authority_boundary"],
  "synthesis": "A failure in an indispensable dimension defeats the release claim; other weaknesses require targeted repair and rerun.",
  "result_authority": "Behavioral evidence for build and regression decisions under the recorded runtime; not commercial approval."
}
```

Required meanings:

- `format` is exactly `cd-augment-eval/v1`.
- `package_version` binds the cases to the package they examine.
- `episode_mode` is `isolated` in v1. Interactive or multi-turn work remains one isolated case.
- `files` lists every suite file once, by filename, with no path traversal.
- `indispensable_dimensions` names behaviors that easier successes cannot average away. Every named dimension must appear in at least one case.
- `synthesis` states how case evidence combines and what defeats the claim.
- `result_authority` states the decision the evidence may inform and the authority it does not possess.

### Suite file

```json
{
  "format": "cd-augment-eval/v1",
  "suite": "core-transfer",
  "package_version": "1.0.0",
  "skills": ["skills/operator/SKILL.md"],
  "runtime": "Isolated episode with only the named package resources and explicitly supplied host capabilities.",
  "claim": "The operator preserves the decisive distinction and changes action when that condition changes.",
  "synthesis": "Both cases must demonstrate the shared competency; the authority-boundary case is indispensable.",
  "cases": [
    {
      "id": "CORE-001",
      "concern": "Sparse but sufficient input",
      "dimensions": ["useful_intake", "authority_boundary"],
      "input": "The user-visible episode begins here.",
      "expected_behaviors": [
        "Observable behavioral invariant required for success."
      ],
      "acceptable_variation": [
        "Competent alternative phrasing or sequence that preserves the invariant."
      ],
      "failure_signals": [
        "Observable seductive failure that materially defeats the competency."
      ]
    }
  ]
}
```

Required meanings:

- `format` repeats the canonical identifier so a suite remains self-describing.
- `suite` is a stable local suite name.
- `package_version` matches the manifest.
- `skills` lists the package-relative skill entry points active in the episode. Use `SKILL.md` for a root-installed skill.
- `runtime` states package resources, tools, host capabilities, context, and authority actually available.
- `claim` names the behavioral proposition examined by this suite.
- `synthesis` states how its cases combine without averaging away indispensable failure.
- `cases` contains one or more isolated episodes.

### Case

Every case includes:

- `id`: unique across the package and stable while the protected behavior remains.
- `concern`: optional short evaluator orientation; never shown to the subject as an answer cue.
- `dimensions`: one or more capability-native behavioral dimensions.
- `input`: the complete initial subject-facing episode.
- `available_on_request`: optional non-empty string describing withheld information released only when the agent asks or acts appropriately.
- `expected_behaviors`: one or more observable invariants, decisions, resource uses, state changes, actions, restraints, handoffs, or completion behaviors.
- `acceptable_variation`: an array, empty when none needs naming, that protects competent alternatives from sample-answer mimicry.
- `failure_signals`: one or more observable failures consequential enough to alter the verdict.

Use these exact field names. Add task-native fields only when they preserve evidence the evaluator or a later handoff genuinely uses. New field names extend the case; they do not replace the canonical ones.

## Preserve the evaluator boundary

The evaluated agent receives package material and `input`, plus withheld information only through the declared interaction. It never receives `expected_behaviors`, `acceptable_variation`, `failure_signals`, `concern`, indispensable gates, or synthesis rules.

Judge observable invariants rather than wording resemblance. Bind every result to package version, host, model, adapter, context, capability, and trial. Preserve raw responses and interventions closely enough to review the verdict.

## Hold legacy formats at the reader

The shared testbed may read historical Testforge, SOP Augment v0.2, and older legacy shapes through compatibility adapters. New builders emit only `cd-augment-eval/v1` unless an approved specification or target runtime explicitly requires another contract.

When rebuilding a legacy package without a format migration mandate, preserve its customer contract and label the evidence dialect honestly. When creating a new release or deliberately migrating, write the canonical manifest and suite fields; do not mint a third local dialect.
