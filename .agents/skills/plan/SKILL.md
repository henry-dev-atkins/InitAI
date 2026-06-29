---
name: plan
description: Use when the prompt contains [PLAN], or when work needs a written plan before editing, testing, validation, or implementation.
---

# [PLAN]
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
- Plans must contain a [PLAN.TERMINAL_CONDITION] section, which defines the conditions under which the plan is considered complete and the agent can exit goal mode through either `[DONE]` or `[BLOCKED]`. 



# Every plan should start with a required block
```
# Plan: <short name>
## Work Classification

- Primary Work Type: `CAPABILITY.RESEARCH`
- Authority:
  - Spec: `AI_SPACE/SPEC.md`, section `<section>`
  - Prompt: `<relevant human instruction>`
- Counts as capability progress: yes
- Commit policy: commit required
- Expected commit prefix: `FEAT:`
- Allowed durable outputs:
  - source code
  - config
  - tests
  - lightweight docs
- Forbidden durable outputs:
  - temporary debug logging
  - one-off plots
  - scratch scripts outside `temp/`
  - local machine-specific paths
- Supporting work allowed:
  - `TEMPORARY.DIAGNOSTIC` only inside `temp/`
  - `EVIDENCE.VALIDATION` for final checks
- Cleanup before `[DONE]`:
  - remove/archive diagnostic scripts
  - remove temporary logging
  - ensure generated artefacts are in intentional locations
- Done gate:
  - implementation exists
  - validation command passes
  - `[SPEC_REVIEW]` passes


- assumptions, 
- key tradeoffs, 
- unresolved risks  
- follow-up work

- Overengineering
- Minimalism - the smallest coherent repo change that directly advances the requested outcome
- Technical debt
- Redundant iterations
- More elegant implementation?
- Dream framework?
- Regressed?
- Gaps?
- Ambiguity?
- Contradictions?
- [PLAN.TERMINAL_CONDITION]
- executive summary
```