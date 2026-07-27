---
name: spec-implement
description: Use when the prompt contains [SPEC.IMPLEMENT] or [SPEC_IMPLEMENT], or when goal mode requires you to implement a spec.
---

# [SPEC.IMPLEMENT] / [SPEC_IMPLEMENT]


The `[TERMINAL_CONDITION]` is a perfect `[SPEC.REVIEW]` from 6 parallel agents.

Do not exit, return to the user, or stop unless the terminal condition is met.

## The Loop

Iterate through stages:
0. `[SPEC.REVIEW]` whole repo.
1. `[PLAN]`
    1. Apply `[WORK_TYPE]`.
    2. Write a plan.
    3. Run `[PLAN.REVIEW]`.
2. Implement through the assigned write-capable agent/s.
3. Test/validate.
4. Review:
    1. `[SPEC.REVIEW]` implementation diff
    2. Defensibility
    3. Plan completeness
    4. Work Type/commit policy
    5. Git commit implementation
5. Either `[DONE]` is justified, or return to step 1 and repeat.

- Use agents for planning, plan review, spec review, defensibility review and plan completeness review when agentic support is available.
- Loops contain one cycle of 0->5. 
- Commits shoudl be made at least once per loop or per implemented plan depending on the dependence between the implementation streams.
- If a loop gets stuck, you have recovery options to carefully choose from by listing pros/cons of each and deciding:
  - Store a broken implementation as an intermediate fix for the next loop's to fix through its own 0->5 cycle. (Small problems).
  - Revert these changes if the other work in the cycle does not depend on it or if it is actually wrong and will need. (Big problems).
- Agent/worker output (`[DONE]`/`[BLOCKED]`, etc) is never the output for the spec-implementation, it is local to the agent.