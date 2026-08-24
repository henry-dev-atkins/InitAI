# Agent Task Packet

## Identity

- Workstream ID: WSXXX
- Plan ID: PXXX
- Agent: {agent-name}
- Parent session: session__YYYYMMDD_HHMMSS
- Primary Work Type: `{WORK_TYPE}`
- Workflow class: SMALL | STANDARD | CAMPAIGN
- Source findings: FXXX
- Requirement IDs: REQXXX
- Accepted plan: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/plan.md`
- Command manifest: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/plan_command_manifest.json`
- Evidence ledger: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/evidence_ledger.json`
- Baseline snapshot: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/baseline_snapshot/`
- Scope diff: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/scope_diff.json`

## Mission and authority

{one coherent spec-aligned outcome}

- Spec authority: {exact section/requirement}
- Required resolution evidence: {evidence}

## Scope

Write scope:
- `{exact repo-relative file or directory root}`

Stable read assumptions:
- `{exact repo-relative file or directory root-or-none}`

Contracts changed:
- `{CON ID-or-none}`

Contracts consumed:
- `{CON ID-or-none}`

Mutable resources:
- `{stable resource ID-or-none}`

Off-limits:
- `AI_SPACE/SPEC.md` unless explicit spec-edit authority is present
- every file not listed in write scope

## Execution policy

- Work in the current checkout.
- Implement the accepted plan only.
- Follow the command manifest.
- Run the manifest through `.agents/skills/orchestrator/scripts/run_command_manifest.py` so the runner writes the evidence ledger.
- Do not write or edit execution claims in the evidence ledger manually.
- Do not broaden the workstream or choose future work.
- Do not create/switch branches or worktrees, merge, rebase, stage or commit.
- Do not ask for repeated command permissions. Use allowed repo-local tools.
- On pre-edit write/tool failure, report `PERMISSION_BLOCKED` with the exact failed operation.
- Leave no temporary diagnostics, fluff, workarounds or unrelated changes.
- Do not include `next_step` or recommendation fields.

## Validation gate

- `{command_id}` proves `{REQ ID / requirement / behaviour}`

## Return contract

Return the result-packet schema with changed files, exact command IDs, validation evidence, scope deviations, unexpected discoveries, evidence ledger path and packet-local status. The orchestrator derives the actual scoped diff from the baseline snapshot.
