---
name: current-state-capsule
description: Use when the prompt contains [CURRENT_STATE], or when the orchestrator needs a compact non-authoritative snapshot of current workflow state.
---

# [CURRENT_STATE]

Create or review a compact current-state capsule for workflow continuity. The capsule is a cache, not spec authority and not product capability.

## Inputs

- current git revision and working tree status;
- latest session board;
- finding register;
- workstream register;
- locks;
- latest review or alignment summary when present.

## Required content

- current revision and dirty-state summary;
- active session path;
- open blockers;
- active and ready workstreams;
- accepted workstreams;
- latest alignment estimate when evidenced;
- active locks and write scopes;
- deferred validation or missing artefacts;
- clear statement that `AI_SPACE/SPEC.md` remains authority when present.

## Rules

- Do not invent alignment estimates or missing register state.
- Do not mark unresolved work as complete.
- Do not include secrets, logs with credentials or large pasted artefacts.
- Do not create placeholder capsules as deliverables.

## Output

```yaml
current_state_capsule_id: CSCXXX
status: DONE | BLOCKED
capsule_path: {path}
source_paths:
  - {path}
unresolved_or_missing_sources:
  - {path-or-none}
```
