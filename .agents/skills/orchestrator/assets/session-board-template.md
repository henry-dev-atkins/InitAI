# Session Board: session__YYYYMMDD_HHMMSS

## Mission

{one-paragraph mission}

## Active constraints

- Spec/prompt source:
- Current checkout:
- Parent permission mode:
- Repository trusted: yes/no
- Available GPU:
- Commit policy: one optional final orchestrator commit

## Work packages

| Plan ID | Primary Work Type | Owner Agent | Files in Scope | Depends On | Integration Order | Status |
|---|---|---|---|---|---|---|
| P001 | {WORK_TYPE} | {agent} | {paths} | none | 1 | PLANNED |

## File ownership rule

Parallel write packages must have disjoint file scopes. Any overlap is serialised in Integration Order.

## Global done gate

- All accepted packages validated.
- Accumulated checkout reviewed.
- Final `[SPEC.REVIEW]` complete.
- No write agent is permission-blocked.
- No unhandled temporary artefacts remain.

## Stop conditions

- Parent turn is read-only.
- Project config/rules are not loaded because the repository is untrusted.
- Required authority/tooling/data is unavailable.
- Validation repeatedly fails without new diagnostic evidence.
