# Agent Task Packet

## Identity

- Plan ID: PXXX
- Agent: {agent-name}
- Parent session: session__YYYYMMDD_HHMMSS
- Branch/worktree: codex/PXXX-{short-name}
- Primary Work Type: `{WORK_TYPE}`

## Mission

{smallest coherent spec-aligned change}

## Authority

- Spec sections:
  - `AI_SPACE/SPEC.md#{section}`
- Human prompt:
  - `{exact relevant instruction}`
- Parent plan:
  - `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/plan__PXXX__short-name/plan.md`

## Scope

Files allowed:
- `{path}`

Files off-limits:
- `AI_SPACE/SPEC.md` unless `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` is present
- unrelated subsystems
- root-level generated artefacts

## Required Skills

Use:
- `$work-type`
- `$plan`
- `$plan-review`
- `$terminal-condition`
- `$spec-review`
- `$final-report`

May call:
- `$diagnose`
- `$monitor`
- `$learn`

## Subagent Policy

You may spawn subagents only for:
- read-only codebase exploration
- diagnosis
- plan review
- spec review
- validation review

You may not spawn write-capable subagents unless this packet explicitly authorises a nested implementation subplan.

## Implementation Policy

- One primary purpose only.
- No broad rewrites.
- No legacy support.
- No workaround scripts.
- No temporary diagnostics left behind.
- Commit only on your owned branch/worktree after validation passes.
- Do not merge to the main branch.

## Validation Gate

Run:
- `{repo-standard-check}`
- `{real-run-command-if-applicable}`

Report:
- commands
- outputs
- changed files
- unresolved issues
- commit hash, if committed

## Return Contract

Return a result packet matching `assets/result-packet-template.md`.
