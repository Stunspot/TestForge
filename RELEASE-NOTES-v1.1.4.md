# TestForge v1.1.4

Version 1.1.4 synchronizes the public operator policy body with the current Nova/MIND distribution. Its shorter discovery description preserves Claude's 200-character host limit; that host-facing line is intentionally not byte-identical to the installed Nova/MIND description.

## Changed

- Synchronizes the software-verification operator with the current TestForge last-tripwire contract: product defects and unfinished requirements return to builder custody instead of turning verification into a repair workshop.
- Aligns the portable Augment, Codex plugin, Claude archives, evaluation metadata, and customer documentation on version 1.1.4.
- Restores deterministic one-family packaging with POSIX archive paths, exact source inventories, nested-archive verification, and a detached SHA-256 digest.
- Ships the independent reviewer as its actual self-contained package instead of duplicating the full operator estate inside it.
- Adds explicit disable, removal, and rollback procedures for Codex and Claude distributions.

## Evidence boundary

Static verification, repository tests, archive parity, documentation review, and the recorded host checks are separate claims. The release does not claim that a copied package is installed, discoverable, invoked, or healthy until that state is directly observed.
