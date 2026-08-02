# TestForge line-ending policy gate

This composite action verifies the repository's committed Git line-ending contract before a change can merge. It supports two profiles:

- Standard: LF-authored text, CRLF `.bat`/`.cmd` working-tree exceptions, binary `-text` rules, and a matching EditorConfig baseline.
- Byte custody: a root `* -text` contract for repositories whose tracked bytes must remain untouched.

The verifier inspects effective Git attributes and the Git index. Scoped `-text` paths remain exempt from CR-byte rejection, so release snapshots and canonical byte trees can retain intentional bytes.

## Caller workflow

Pin the action to a reviewed TestForge commit:

```yaml
name: TestForge line-ending policy

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  line-ending-policy:
    name: line-ending-policy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: Stunspot/TestForge/line-ending-policy@REPLACE_WITH_REVIEWED_COMMIT_SHA
```

Make the `line-ending-policy` job a required status check on the default branch. The workflow detects violations; the GitHub ruleset prevents them from landing.

## Local command

```text
python -B tools/verify_line_endings.py --root PATH_TO_REPOSITORY
```

The command returns JSON and exits nonzero for a policy violation or inspection error.
