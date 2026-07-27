# Agent Task Packet

## Identity

- Workstream ID: WSXXX
- Plan ID: PXXX
- Agent: {agent-name}
- Parent session: session__YYYYMMDD_HHMMSS
- Primary Work Type: `{WORK_TYPE}`
- Source findings: FXXX
- Accepted plan: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plan.md`

## Mission and authority

{one coherent spec-aligned outcome}

- Spec authority: {exact section/requirement}
- Required resolution evidence: {evidence}

## Scope

Write scope:
- `{path}`

Stable read assumptions:
- `{path-or-none}`

Contracts changed:
- `{interface/schema/config/output-or-none}`

Contracts consumed:
- `{interface/schema/config/output-or-none}`

Off-limits:
- `AI_SPACE/SPEC.md` unless explicit spec-edit authority is present
- every file not listed in write scope

## Execution policy

- Work in the current checkout.
- Implement the accepted plan only.
- Do not broaden the workstream or choose future work.
- Do not create/switch branches or worktrees, merge, rebase, stage or commit.
- Do not ask for repeated command permissions. Use allowed repo-local tools.
- On pre-edit write/tool failure, report `PERMISSION_BLOCKED` with the exact failed operation.
- Leave no temporary diagnostics, fluff, workarounds or unrelated changes.
- Do not include `next_step` or recommendation fields.

## Validation gate

- `{command}` proves `{requirement/behaviour}`

## Return contract

Return the result-packet schema with changed files, commands, exact results, validation evidence, scope deviations, unexpected discoveries and packet-local status.
