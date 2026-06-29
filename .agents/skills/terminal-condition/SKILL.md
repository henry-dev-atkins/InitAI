---
name: TERMINAL_CONDITION
description: Use when the prompt includes [TERMINAL_CONDITION] or goal mode requires plan, implementation, validation, review, and iteration until [DONE] or a genuine [BLOCKED] state.
--- 

# Workflow

`[TERMINAL_CONDITION]`: Do not 'exit', 'return to user', 'apply `<|endoftext|>`' or similar unless `[TERMINAL_CONDITION]` is met.
  Iterate through stages:
  1. Plan
      1a. Write a plan
      1b. Review of plan
  2. Implement
  3. Test
  4. Review
      4a. `[SPEC_REVIEW]`
      4b. Defensibility
      4c. Plan completeness
  5. Either `[TERMINAL_CONDITION]` is met, or return to step 1 and repeat the loop.
  - Use agents for 1a, 1b, 4a, 4b and 4c.
  - Early exit is allowed only for a genuine `[BLOCKED]` state, including:
      - a safety/authority issue would place too much responsibility on the AI
      - required access/tooling/data is unavailable
      - the human instruction conflicts with the spec and cannot be resolved safely
  - Repeat until `[DONE]` or a genuine `[BLOCKED]` state.
  - Early exit is never `[DONE]`.
  - Do not blow up, delete or make widespread edits in this loop.
  - You may call on `[DIAGNOSE]`, `[SUBPLAN]` or `[MONITOR]` at any point.
  - If any iteration ends with a named shortfall instead of a working validated result, return to step 1 or call `[DIAGNOSE]`.
  - Example applications:
      - Implement perfect SPEC alignment. Over iterations the repo will converge to the spec.
  - This is the same as a goal, any `[TERMINAL_CONDITION]` usage is within a goal, it is not the end goal.
  
## Progress guard:
- If the same failure recurs after a repair attempt, stop patching reactively and run `$diagnose`.
- If no new evidence or implementation progress is produced across a full loop, report `[BLOCKED]` with the exact missing authority/tooling/data rather than spinning.
- Do not make broad edits just because the loop continues.