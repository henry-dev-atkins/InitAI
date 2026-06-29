# Session Board: session__YYYYMMDD_HHMMSS

## Mission

{one-paragraph mission}

## Active Constraints

- Spec source: `AI_SPACE/SPEC.md`
- Current branch:
- Available GPU:
- Human flags present:
- Commit policy:
- Forbidden work today:

## Dependency Graph

1. {P001 dependency statement}
2. {P002 dependency statement}

## Work Packages

| Plan ID | Primary Work Type | Owner Agent | Branch/Worktree | Files in Scope | Depends On | Merge Order | Status |
|---|---|---|---|---|---|---|---|
| P001 | {WORK_TYPE} | {agent} | codex/P001-{short-name} | {paths} | none | 1 | PLANNED |

## GPU / Resource Schedule

| Plan ID | Resource | Scheduling rule |
|---|---|---|
| PXXX | GPU | serial only |

## Global Done Gate

- All accepted plans validated.
- Worker branches either merged or explicitly staged for human review.
- Final `[SPEC.REVIEW]` complete.
- Final `[LEARN]` run where relevant.
- Final `[SESSION.END]` run if ending session.

## Stop Conditions

- Spec conflict cannot be resolved.
- Required authority/tooling/data is unavailable.
- Two write packages require the same files and cannot be serialised safely.
- Validation repeatedly fails without new diagnostic evidence.
