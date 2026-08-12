# Install TestForge in Codex

## Choose an installation path

For the public Codex plugin, run the two marketplace commands shown in the repository [README](../../README.md), then start a new Codex task. For standalone skills, copy the complete `skills/software-verification/` and `skills/verification-reviewer/` folders into the personal Codex skills directory. On Windows, each final path normally ends in `.codex\skills\<skill-name>\SKILL.md`.

Keep every folder intact. The operator needs its doctrine, templates, examples, fallbacks, and scripts; the reviewer needs its adversarial checks, rubric, and validators. A lone `SKILL.md` is not a complete installation.

## Verify discovery

1. Start a new Codex task after installation.
2. Invoke `$software-verification` and ask it to identify the verification intake it needs.
3. Start another fresh task and invoke `$verification-reviewer` against an existing or synthetic verification package.
4. Confirm each skill can reach its referenced resources.

Success for one skill does not prove the other is installed. If either skill does not appear, preserve the visible symptom, verify the final folder or plugin state, restart Codex, and follow [Troubleshooting](TROUBLESHOOTING.md) before rebuilding the package.
## Update

Before replacing anything, record the installed TestForge version and preserve any verification manifests or evidence you intend to keep. For the marketplace plugin, use the host's plugin manager to remove the installed `testforge@cd-testforge` entry, then run the two current marketplace installation commands again and start a new task. For standalone skills, replace both complete skill folders from the same release; do not mix operator and reviewer versions.

Repeat both discovery probes after every update. An updated file tree does not establish that a running task loaded the new version.

## Remove and clean up

For the marketplace path, remove `testforge@cd-testforge` through the Codex plugin manager and start a new task to confirm both TestForge handles are absent. For standalone installation, delete only the two exact installed folders named `software-verification` and `verification-reviewer` after resolving their full paths; do not remove the surrounding skills directory.

TestForge has no service account, telemetry store, daemon, or product database to delete. Verification manifests, reports, raw command captures, test files, promoted baselines, and evaluation runs are ordinary local project artifacts. Review them for retention, then archive or delete them under the project's own data policy. Removing TestForge does not automatically remove those records or any data retained by Codex, configured models, Git hosts, or external tools.
