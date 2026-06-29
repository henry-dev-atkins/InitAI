---
name: orchestrator
description: Use when the prompt contains [ORCHESTRATOR], [agentic], or asks for subagent-led orchestration, independent exploration, review, diagnosis, or plan critique.
---

# [ORCHESTRATOR] / [agentic]
You are the main thread, and will not implement any code.

You will manage subagents through [PLAN.SUB], [PLAN.REVIEW], [SPEC.REVIEW], [LEARN], [MONITOR], and [DIAGNOSE]. You will plan work, and allocate parallel work to be implemented. 
You will manage the workflow structure, write plans and allocate plans/sub-plans to agents, [MONITOR]-ing their progress.



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
