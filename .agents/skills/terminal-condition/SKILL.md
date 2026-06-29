---
name: terminal-condition
description: Use when the prompt contains [PLAN.TERMINAL_CONDITION] or [TERMINAL_CONDITION], or when goal mode requires plan, implementation, validation, review, and iteration until [DONE] or a genuine [BLOCKED] state.
---

# [PLAN.TERMINAL_CONDITION] / [TERMINAL_CONDITION]

Do not exit, return to the user, or stop unless the terminal condition is met.

Iterate through stages:

1. `[PLAN]`
    1. Apply `[WORK_TYPE]`.
    2. Write a plan.
    3. Run `[PLAN.REVIEW]`.
2. Implement.
3. Test/validate.
4. Review.
    1. `[SPEC.REVIEW]`
    2. Defensibility
    3. Plan completeness
    4. Work Type/commit policy
5. Either `[DONE]` is justified, or return to step 1 and repeat.

Use agents for planning, plan review, spec review, defensibility review and plan completeness review when agentic support is available.

## Early exit

Early exit is allowed only for a genuine `[BLOCKED]` state, including:

- a safety/authority issue would place too much responsibility on the AI
- required access/tooling/data is unavailable
- the human instruction conflicts with the spec and cannot be resolved safely
- an agent/subagent cannot be started or restarted and the work genuinely needs it

Early exit is never `[DONE]`.

## Progress guard

- If the same failure recurs after a repair attempt, stop patching reactively and run `[DIAGNOSE]`.
- If no new evidence or implementation progress is produced across a full loop, report `[BLOCKED]` with the exact missing authority/tooling/data rather than spinning.
- Do not make broad edits just because the loop continues.
- Do not preserve a shortfall as a named category; close it, re-plan or block.

## Orchestrated goal mode

In `$orchestrator` mode:

- Worker `[DONE]` means the worker packet is done, not the session.
- Session `[DONE]` requires merge/integration review, accepted branch state, global validation and final `[SPEC.REVIEW]`.
- If a worker reports `[BLOCKED]`, the orchestrator must decide whether to repair, reassign, split, defer with human approval, or block the session.
