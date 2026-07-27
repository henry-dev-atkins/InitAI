---
name: terminal-condition
description: Use when the prompt contains [PLAN.TERMINAL_CONDITION] or [TERMINAL_CONDITION], or when goal mode requires plan, implementation, validation, review, and iteration until [DONE] or a genuine [BLOCKED] state.
---

# [PLAN.TERMINAL_CONDITION] / [TERMINAL_CONDITION]

Do not exit, return to the user, or stop unless the terminal condition is met.

## Early exit

Early exit is allowed only for a genuine `[BLOCKED]` state, including:

- a safety/authority issue would place too much responsibility on the AI
- required access/tooling/data is unavailable
- the human instruction conflicts with the spec and cannot be resolved safely
- an agent/subagent cannot be started or restarted and the work genuinely needs it

Early exit is never `[DONE]`.


## Correct Exit

A suite of 6 agnets needs to each independnatly and holistically confirm that a condition has been met. Procedure is sequential though to minimise wasted worker time.