# Promoted Augment evaluation baselines

This directory contains compact, reviewed baseline records produced by `augment_eval.py promote`.

Each baseline records the package identity, model and host, harness and adapter provenance, review status, run-integrity identity, and complete numerical summary. It deliberately excludes raw prompts and transcripts; those remain in the local `evaluation-results/` testbed.

Updating an existing named baseline requires `--replace` so movement of the reference point is deliberate and visible in version control.
