---
name: PLAN_SUB
description: A Plan requries a previous plan contains work which is too large to be 'a part of a plan'. This skill allows for a plan to be split into subplans, which can be worked on in parallel or sequentially. The subplan is a temporary aside, and the agent will return to the original plan after the subplan is completed.
--- 

# Plans
- Planning should be done considering all layers of the project. Get as much of the documentation & code into your context as possible to minimise errors.
- All plans should consider consequences, for example:
    - If a variable changes type, where is it used? Do we still assume the old type anywhere?
- All plans require explicit, agentic plan reviews for:
    - Overengineering
    - Minimalism - the smallest coherent repo change that directly advances the requested outcome
    - Technical debt
    - Redundant iterations (smoke tests, small examples, etc)
    - Is there a more elegant implementation that I missed?
    - Is this code a true implementation of the dream framework?
        - Have I regressed to a non-correct implementation?
    - Have I left gaps, ambiguity or contradictions?
- Plans guide execution; plans are not deliverables unless the human explicitly requested plan-only output.
- Plan reviews must feed back into implementation. Do not stop at "plan reviewed".
- Plans must state assumptions, key tradeoffs, unresolved risks and follow-up work.
- Final reports may state follow-up work only after `[DONE]`, `[BLOCKED]`, or human-approved deferral. Follow-up work is not closure.
- All plans should end in a short, human-facing executive summary of the work. The summary is not a terminal condition.
- Plans are reviewed bottom up by humans scrolling up through the terminal, not top down.
- If a plan implementation will/does end with "X helped only a little, but Y is still the real blocker":
    - it is a planning/diagnosis failure, so stop, re-`[DIAGNOSE]`, and re-plan before planning/implementing more.
- Plans must be written according to the workflow structure:
```
sessions/
    - session__YYYYMMDD_HHMMSS/
      - plan__YYYYMMDD_HHMMSS/
        - plan.md
```


We are marking an aside. Name the plan which we were working on before as `[PLAN_A]` and write a new, subplan `[PLAN_B]` to temporarily switch to.
    - We will switch back to `[PLAN_A]` immediately after `[PLAN_B]` completion.