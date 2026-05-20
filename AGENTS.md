# Agents.md
Our spec is at `AI_SPACE/SPEC.md`.


# Rules:
- No secrets in code
- No secrets in logs, configs, handovers or artefacts
- No Spec reqriting unless key: `[SPEC EDIT REQUIRED]` is present
- SPEC misalignment must be IMMEDIATLY raised with maximum verbosity and significance
    - If a human/prompt drifts from the spec please highlight and clarify that this was intentional (humans make mistakes, but also change their mind - find out which)
- Any operations outside the main folder/repo require detailed reports on why you need to do it.
- Never delete any file/folder: All file/folder deletions are not actual deletions, but a move to an `archive/` folder.
- No invented files, paths, modules or commands: check first, then reference
- No silent fallback behaviour
- No placeholders
- No silent GPU to CPU fallback
- No ad hoc output sprawl across the repo root
- No silent errors or quietly unsupported behaviour
- UK English spelling not US-english
- No editing anything outside the working repo/folder unless given the [EXTERNAL_EDIT_ALLOWED] flag, even then: NO DELETIONS EVER.
- Every new dependency needs justification
- Forbidden terminology:
    - Canonic (ise/al)
    - Version X
    - Word soup. e.g.:
        - "First Class/Canonical Remote Run Root", -> "Entry point"
        - "extend the real behavioural test to do XYZ", -> "Add tests for XYZ"
        - "refresh one clean Session 1 proof package with matching identities" -> "Session 1 runs successfully"
        - "refuse to declare closure while any split proof surface or command-surface mismatch remains" -> "refuse to claim closure unless proven"
    - Placeholder
    - Honest
- Your space is `AI_SPACE/`, with folders for:
    - `plans/` store every plan you generate (timestamp in name)
    - `handovers/` context dump of the work for tomorrow
    - `AI_LEARNINGS_LOG.md` store lessons, mistakes and vital information you pick up through work. Keep it clean.
    - `TODO.md` is a rolling store of tasks that you add to, align with `plans/` and use for progress tracking. Do not delete elements. 
- If 'agentic' is requested, fire up an agent for it. [agentic]: use a standalone independant agent.
- All code must run from inside your sandbox/repo, no 'external' runs.

# Guide:
- Favour simplicity - no overengineering
- Fail fast, frequently and with maximum explainability - learn from mistakes in an 'AI_LEARNINGS_LOG.md'
- We have access to one GPU locally (RTX 5090)
- Config driven research means that implementing new classes etc should be easy
- Keep it Simple, Stupid!
- Keep temporary files (`.ruff_cache/`, `.triton_tmp/`) inside `temp/` to minimise clutter
- No 'Smoke Tests', minimal 'dry runs' in the main codebase - we are a research project not a software company
    - Use the `temp/` file for any intermediate/dev work that is needed
- Test only valuable, behavioural logic, not basic stuff
- GPUs for ML, not CPU
- Unsupported GPU, CUDA or device situations must fail loudly and clearly
- Call out expected performance, VRAM or RAM impact when it is materially affected
- The best tests (correctness checks etc) are real runs, and should be done at the end of plans
    - MNIST CNN 100 epochs, not a small simulated dataset - at the end
    - Analysis library correctly plots real runs, not fake simulated runs
    - MNIST CNN 5 epochs, not a small simulated dataset - at intermediate development steps/checks
- Never support legacy work
    - We are 'current state only' not v0, v1, v2
    - In the case of a change, change the code, do not wrap old logic
    - Do not support or maintain legacy logic or backwards compatability
    - No 'patching' we only 'do'
    - Only 'Canonical' work, no 'non-canonical' work.
- Config should be the source of truth for experiment behaviour
- Avoid hardcoded experiment values when config should own them
- New features should slot cleanly into the config structure
- Generated artefacts should go to clear, intentional output locations
- Large datasets and checkpoints should follow repo storage conventions and must not be casually committed
- Prefer repo-standard tools and commands over ad hoc alternatives
- Efficiently design entry points to minimise permission/approval delays
    - Config driven runs may be needed inside a run command, can we pre-approve 'any' config given a runner we trust?
- No workarounds
    - No honest placeholders
    - No documented gaps
    - No lazyness
    - No cosmetic completion
    - If you end a prompt with a phrase like 
        - "the remianing work is..." 
        - "X helped only a little, but Y is still the real blocker"
        - then you probably have broken this guideline - therefore, return to work


# Commands
- [SESSION.START]: Teach me the project, philosophy, goals, idea and then note down progress, last steps, current steps, next steps.
- [SESSION.CLEAN]: Move clutter/fluff/noise from repo into the `archive/` folder, or move files into their correct place.
    - Look for old-(handovers, progress reports, intermediate results, etc) 
- [SESSION.END]: Update docs, learnings, to-do's, progress and write a detailed handover note (name = todays date & time) for full reproducibility.
    - Include: what changed, why, exact commands run, results, current state, open issues and next steps
- [SUBPLAN]: We are marking an aside. Name the plan which we were working on before as [PLAN_A] and write a new, subplan [PLAN_B] to temporarily switch to.
    - We will switch back to [PLAN_A] immediatly after [PLAN_B] completion.
- [LEARN]: Review learnings and map them to documentation.
    - Some learnings may be outdated, so please ask me which lessons to forget.
    - Make surgical doc/spec (request edit permissions) updates of the learnings.
    - Empty the learnings table for next time.
    - Commit this work so we preserve learnings.
- [MONITOR]: A script is running and will output logs/pregress/results which you need to await->evaluate->maybe intervene->await->...
    - Spec alignemnt is first priority, do not drift away through iterations.
    - Generally this is needed when the script is 'right' but just needs debugging/diagnosing etc.
- [DIAGNOSE]: What is the underlying cause of this symptom?
    - No band-aid, hacky or workaround fixes
    - You may use agents for diagnostic experiments
    - We are experimentally driven, not speculative
    - Agentically consider high level (philosophy, underlying math, etc), medium level (integration, usage, etc) and low level (bugs, syntax, etc).
- [TERMINAL_CONDITION]: Do not 'exit', 'return to user', 'apply `<|endoftext|>`' or similar unless [TERMINAL_CONDITION] is met, iterate through stages:
    1. Plan
        1a. Write a plan
        1b. Review of plan
    2. Implement
    3. Test
    4. Review
        4a. [SPEC_REVIEW]
        4b. Defensibility
        4c. Plan completeness
    5. Either [TERMINAL_CONDITION] is met, or return to step 1 and repeat the loop.
    - use agents for 1a, 1b, 4a, 4b and 4c. 
    - Early exit may be allowed when:
        - something happens to place too much resposibility on the AI 
    - Do not blowup, delete or make widespread edits in this loop
    - You may call on [DIAGNOSE], [SUBPLAN] or [MONITOR] at any point
    - Example appliations:
        - Implement perfect SPEC alignment. Over iterations the repo will converge to the spec.
- [SPEC_REVIEW]: Compare implementation to the specification (May be a subset of spec).
    - Check alignment agentically by type:
        - Logic
        - Implementation
        - Correctness
        - Documentation
        - Outputs
        - Defensibility 
        - Lazyness


# SPEC Usage
- Spec will have a walkthrough section with work stages/steps/milestones.
- Spec doc is generally the guide to build the project, not it's usage, for example:
    - The steps to build a reserach suite, not the actual experiments.
    - The steps to build an app, not the actual app itself.
- The 'usage' comes later, and generally the spec is swapped out for an explicit 'implementation guide'.


# Learnings
- Update `AI_SPACE/AI_LEARNINGS_LOG.md` after
    - failures, 
    - debugging discoveries or 
    - architecture/course corrections
    - mistakes
- Update `AI_SPACE/TODO.md` only with concrete unresolved follow-up work
- Do not fill TODOs with vague ideas, duplicates or already-completed work
- Always run the [LEARN] operation when updating


# Plans
- Planning should be done considering all layers of the project (get as much of the documentation & code into your context as possible to minimise errors)
- All plans should consider consequences, for example:
    - If a variable changes type, where is it used? Do we still assume the old type anywhere?
- All plans require explicit, agentic plan reviews for:
    - Overengineering
    - Technical debt
    - Redundent iterations (smoke tests, small examples, etc)
    - Is there a more elegant implementation that I missed?
    - Is this code a true implementation of the dream framework?
        - Have I regressed to a non-correct implementation?
    - Have I left gaps, ambiguity or contradictions?
- Plans and final reports must state assumptions, key tradeoffs, unresolved risks and follow-up work
- All plans should end in a short, human facing executive summary of the work.
- Plans are reviewed bottom up by humans scrolling up through the terminal, not top down.
- If a plan implementation will/does end with "X helped only a little, but Y is still the real blocker":
    - it is planning/diagnosis failure so stop, re-[DIAGNOSE], and re-plan before planning/implementing more


# Done Means
- The code change is complete, coherent and aligned with the spec or explicit human instruction
- Relevant checks or real runs have been completed at the right stage
- Config, docs and outputs have been updated where behaviour changed
- Obsolete assumptions and replaced logic in touched areas have been cleaned up
- Learnings, TODOs and handovers have been updated when relevant
- The remaining limitations and next steps are clearly stated

- Required spec alignment passes a [SPEC_REVIEW].
- A plan's implementation is complete, with no-gaps, no suprises, no lazyness and no workarounds