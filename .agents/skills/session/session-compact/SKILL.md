---
name: session-compact
description: Use when the prompt contains [SESSION.COMPACT], or when an orchestration session exceeds compaction thresholds and needs a compact current-state handover without deleting active evidence.
---

# [SESSION.COMPACT]

Compact an orchestration session by producing a current-state capsule and compaction manifest. This is workflow hygiene only. It must not delete product files, source evidence, registers or accepted workstream artefacts.

## Trigger conditions

Run compaction after any of:

- active session contains more than 100 versioned `plans/PXXX/` directories;
- active session size exceeds 10 MB;
- a major checkpoint follows a full spec review;
- the orchestrator needs to preserve state before context pressure would make control decisions unreliable.

## Required behaviour

- Read the current session board, canonical finding and requirement registers, workstream and contract registers, and locks.
- Summarise current revision, open blockers, active portfolio, latest alignment estimate when present, accepted workstreams and active locks.
- Record what was summarised, what remains authoritative and what was not inspected.
- Preserve all source artefacts. If material must leave the active tree, move it only to `AI_SPACE/archive/` with a manifest entry.
- Do not treat the capsule as product capability or spec authority.

## Output

```yaml
session_compaction_id: SCXXX
session: session__YYYYMMDD_HHMMSS
status: DONE | BLOCKED
session_capsule_path: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/current_state_capsule.md
global_pointer_path: AI_SPACE/current_state.md
manifest_path: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/reports/session-compaction/SCXXX.md
authoritative_sources:
  - {path}
omitted_or_unread:
  - {path-or-none}
```
