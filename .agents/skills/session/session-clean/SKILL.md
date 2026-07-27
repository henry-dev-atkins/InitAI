---
name: session-clean
description: Use when the prompt contains [SESSION.CLEAN], or when repo clutter, handovers, plans, session boards, TODOs, learnings, temporary artefacts or agent outputs need consolidation without deleting files.
---

# [SESSION.CLEAN]

Move/aggregate clutter/fluff/noise from repo into the `archive/` folder, or move files into their correct place.

Never delete files/folders.

Review:

- TODOs
- handovers
- session boards
- plans and subplans
- result packets
- AI learnings
- temporary diagnostics
- one-off plots/fluff
- obsolete duplicate skill folders

Before moving or aggregating files, use `maintain-declutter` when a report-only commit/archive/move audit is needed. Use `maintain-despaghettify` when cleanup reveals tangled repo/code organisation that should be reviewed before restructuring.

For each entry, label as one or more of:

- CORRECT
- OUTDATED
- INCORRECT
- IRRELEVANT
- DUPLICATE_<CLUSTER_NAME>
- COMPLETED

Collate/aggregate relevant info into the correct document and archive noise.

Ensure the repo is navigable and self-explanatory.
