# Agents.md
Our guide is at `AI_SPACE/SPEC.md`.


# Rules:
- No secrets in code
- No Spec reqriting unless key: `SPEC EDIT REQUIRED` is present
- SPEC misalignment must be IMMEDIATLY raised with maximum verbosity and significance
    - If a human/prompt drifts from the spec please highlight and clarify that this was intentional (humans make mistakes, but also change their mind - find out which)
- Any operations outside the main folder/repo require detailed reports on why you need to do it.
- Never delete any file/folder: All file/folder deletions are not actual deletions, but a move to an `archive/` folder.  

# Guide:
- Favour simplicity - no overengineering.
- Fail fast, frequently and with maximum explainability - learn from mistakes in an `AI_SPACE/AI_LEARNINGS_LOG.md`.
- We have access to one GPU locally (RTX 5090).
- Config driven research means that implementing new classes etc shoudl be easy
- Keep it Simple, Stupid!
- Keep temporary files (`.ruff_cache/`, `.triton_tmp/`) inside `temp/` to minimise clutter. 
- No silent errors or quietly unsupported behaviour
- UK English spelling not US-english 
- No 'Smoke Tests', minimal 'dry runs' in the main codebase - we are a research project not a software company
    - Use the `temp/` file for any intermediate/dev work that is needed
- Test only valuable, behavioural logic, not basic stuff
- GPUs for ML, not CPU
- The best tests (correctness checks etc) are real runs, and should be done at the end of plans.
    - MNIST CNN 100 epochs, not a small simulated dataset - at the end
    - Analysis library correctly plots real runs, not fake simulated runs
    - MNIST CNN 5 epochs, not a small simulated dataset - at intermediate development steps/checks
- Never support legacy work
    - We are 'current state only' not v0, v1, v2
    - In the case of a change, change the code, do not wrap old logic
    - Do not support or maintain legacy logic or backwards compatability 
    - No 'patching' we only 'do'


# Commands
- [SESSION.START]: Teach me the project, philosophy, goals, idea and then note down progress, last steps, current steps, next steps.
- [SESSION.END]: Update docs, learnings, to-do's, progress and write a detailed handover note (name = todays date & time) for full reproducibility.
- [SUBPLAN]: We are marking an aside. Name the plan which we were working on before as [PLAN_A] and write a new, subplan [PLAN_B] to temporarily switch to. 
    - We will switch back to [PLAN_A] immediatly after [PLAN_B] completion.


# SPEC Usage
- Spec will have a walkthrough section with work stages/steps/milestones.


# Plans
- Planning should be done considering all layers of the repo (get as much of the code into your context as possible to minimise errors)
- All plans should consider consequences, for example:
    - If a variable changes type, where is it used? Do we still assume the old type anywhere? 
- All plans require explicit, agentic reviews for:
    - Elegance
    - Holistic/decision-completeness 
    - Overengineering
    - Technical debt
    - Redundent iterations (smoke tests, small examples, etc)
    - Is there a more elegant implementation that I missed?
    - Is this code a true implementation of the dream framework?
        - Have I regressed to a non-correct implementation?
    - Have I left gaps, ambiguity or contradictions?
- All plans must be:
    - Immediatly saved as a timestamped .md file under `AI_SPACE/plans/...`
    - Mapped to elements in TODO.md