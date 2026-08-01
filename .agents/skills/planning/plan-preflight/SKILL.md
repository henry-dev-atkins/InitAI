---
name: plan-preflight
description: Use when the prompt contains [PLAN.PREFLIGHT], or before full plan review to mechanically validate one workstream plan and its command manifest.
---

# [PLAN.PREFLIGHT]

Run a mechanical preflight on one submitted workstream plan before `[PLAN.REVIEW]`. This skill validates structure, command evidence and path hygiene only. It does not judge product intent, choose workflow sequencing or implement changes.

## Inputs

- plan path;
- parent session path;
- source workstream ID;
- expected plan ID;
- expected source finding IDs;
- allowed write scope;
- off-limits scope;
- contracts changed and consumed.

If any required input is unavailable, return `BLOCKED` with the missing authority or file path.

## Required checks

- The plan contains every required `$plan` section.
- Identity fields match the assigned workstream and plan IDs.
- Primary Work Type is present and valid.
- Write scope, off-limits scope, contracts changed and contracts consumed are explicit.
- The `Command Manifest` section is present and parseable.
- Command IDs are unique, stable and referenced by validation evidence.
- Every command declares purpose, working directory, expected status and evidence target.
- Pytest commands use a repo-local `temp/` basetemp.
- Inline Python snippets compile where detectable.
- Referenced files or paths exist when the plan marks them as existing prerequisites.
- No unresolved placeholders appear outside templates.
- No malformed temp/cache roots or paths outside the repository are accepted.

## Output

```yaml
plan_preflight_id: PFXXX
workstream_id: WSXXX
plan_id: PXXX
status: PASS | FAIL | BLOCKED
blocking_issues:
  - criterion: {mechanical-check}
    evidence: {specific defect}
validated_command_ids:
  - {command-id}
```

`PASS` permits `[PLAN.REVIEW]` to start. `FAIL` sends the plan back to replanning with the concrete mechanical defects. `BLOCKED` is only for missing files, authority, tooling or a safe execution path.
