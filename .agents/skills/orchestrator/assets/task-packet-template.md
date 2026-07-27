# Agent Task Packet

## Identity

- Plan ID: PXXX
- Agent: {agent-name}
- Parent session: session__YYYYMMDD_HHMMSS
- Primary Work Type: `{WORK_TYPE}`
- Checkout: current parent-session checkout

## Mission

{smallest coherent spec-aligned change}

## Authority

- Spec/prompt authority: {exact source}
- Parent plan: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/plan__PXXX__short-name/plan.md`

## Scope

Files allowed:
- `{path}`

Files off-limits:
- `AI_SPACE/SPEC.md` unless a spec-edit flag is present
- every file not listed above

## Execution policy

- Work in the current checkout.
- Edit only files in scope.
- Do not create/switch branches or worktrees.
- Do not merge, rebase, stage or commit.
- Do not ask for repeated per-command permissions. If the workspace is not writable, stop and return `PERMISSION_BLOCKED` with the failed operation.
- No broad rewrites, legacy support, workarounds or temporary diagnostics left behind.
- You are not a process manager. Report facts for this packet only. Do not suggest next steps, choose future work, or include `next_step` / `recommended_next_action` fields.

## Validation gate

Run:
- `{repo-standard-check}`
- `{real-run-command-if-applicable}`

## Return contract

Return changed files, commands run, results, unresolved issues, temporary files created/archived and a concise `[DONE]` or `[BLOCKED]` result for this packet. Do not include process-direction text.
