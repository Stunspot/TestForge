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
