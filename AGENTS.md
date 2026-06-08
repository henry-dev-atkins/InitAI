# AGENTS.md
Our spec is at `AI_SPACE/SPEC.md`.


# Rules:
- No secrets in code
- No secrets in logs, configs, handovers or artefacts
- No spec rewriting unless key: `[SPEC EDIT REQUIRED]` is present
- SPEC misalignment must be IMMEDIATELY raised with maximum verbosity and significance
    - If a human/prompt drifts from the spec, highlight it and clarify whether this was intentional. Humans make mistakes, but also change their mind: find out which.
    - Raising misalignment is not the same as finishing the task. After raising it, either continue once alignment is clear or report `[BLOCKED]`.
- Any operations outside the main folder/repo require detailed reports on why you need to do it.
- Never delete any file/folder: All file/folder deletions are not actual deletions, but a move to an `archive/` folder.
- No invented files, paths, modules or commands: check first, then reference
- No silent fallback behaviour
- No placeholders
- No silent GPU to CPU fallback
- No ad hoc output sprawl across the repo root
- No silent errors or quietly unsupported behaviour
- UK English spelling, not US English
- No editing anything outside the working repo/folder unless given the `[EXTERNAL_EDIT_ALLOWED]` flag, even then: NO DELETIONS EVER.
- Every new dependency needs justification
- No documentation-only substitutions for implementation, proof, test or validation work unless documentation-only work was explicitly requested.
- No gap classification or issue taxonomy as a deliverable unless the human explicitly requested diagnosis/taxonomy only.
- Forbidden terminology and phrasing in reports, plans, invented architecture names or task outcomes:
    - Canonic (ise/al)
    - Canonical
    - Version X
    - Word soup. e.g.:
        - "First Class/Canonical Remote Run Root", -> "Entry point"
        - "extend the real behavioural test to do XYZ", -> "Add tests for XYZ"
        - "refresh one clean Session 1 proof package with matching identities" -> "Session 1 runs successfully"
        - "refuse to declare closure while any split proof surface or command-surface mismatch remains" -> "refuse to claim closure unless proven"
    - Placeholder
    - Honest
    - Documented gap
    - Classified gap
    - Proof consolidation gap
- Your space is `AI_SPACE/`, with folders for:
    - `plans/` store every plan you generate (timestamp in name)
    - `handovers/` context dump of the work for tomorrow
    - `AI_LEARNINGS_LOG.md` store lessons, mistakes and vital information you pick up through work. Keep it clean.
    - `TODO.md` is a rolling store of tasks that you add to, align with `plans/` and use for progress tracking. Do not delete elements.
- If 'agentic' is requested, fire up an agent for it. `[agentic]`: use a standalone independent agent.
- All code must run from inside your sandbox/repo, no 'external' runs.


# Guide:
- Favour simplicity - no overengineering
- Fail fast, frequently and with maximum explainability - learn from mistakes in `AI_SPACE/AI_LEARNINGS_LOG.md`
- We have access to one GPU locally (RTX 5090)
- Config driven research means that implementing new classes etc should be easy
- Keep it Simple, Stupid!
- Keep temporary files (`.ruff_cache/`, `.triton_tmp/`) inside `temp/` to minimise clutter
- No smoke tests, minimal dry runs in the main codebase - we are a research project not a software company
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
    - Do not support or maintain legacy logic or backwards compatibility
    - No band-aids: implement the actual change
    - Only current-state work, no alternate-track work
- Config should be the source of truth for experiment behaviour
- Avoid hardcoded experiment values when config should own them
- New features should slot cleanly into the config structure
- Generated artefacts should go to clear, intentional output locations
- Large datasets and checkpoints should follow repo storage conventions and must not be casually committed
- Git commits should start with `CLEANUP:`, `FEAT:`, `CONFIG:`, `DOCS:`, `FIX:`, `TEST:`, `AI:` or `SPEC_EDIT:`
- Prefer repo-standard tools and commands over ad hoc alternatives
- Efficiently design entry points to minimise permission/approval delays
    - Config driven runs may be needed inside a run command, can we pre-approve 'any' config given a runner we trust?
- No workarounds
    - No placeholders/stubs
    - No documented gaps as deliverables
    - No laziness
    - No cosmetic completion
    - A failing command/check is the next repair target, not an endpoint
    - If you end a prompt with a phrase like:
        - "the remaining work is..."
        - "X helped only a little, but Y is still the real blocker"
        - then you have not met the terminal condition; return to work
- When inside \goal mode a `[DONE]` means a small subtask is done, not the goal, so keep iterating.


# Commands
- `[SESSION.START]`: Teach me the project, philosophy, goals, idea and then note down progress, last steps, current steps, next steps.
- `[SESSION.CLEAN]`: Move clutter/fluff/noise from repo into the `archive/` folder, or move files into their correct place.
    - Look for old handovers, progress reports, intermediate results, etc.
- `[SESSION.END]`: Update docs, learnings, to-do's, progress and write a detailed handover note (name = today's date & time) for full reproducibility.
    - Include: what changed, why, exact commands run, results, current state, open issues and next steps
    - Open issues are not closure. If open issues are in-scope, mark `[BLOCKED]` unless the human explicitly deferred them.
- `[SUBPLAN]`: We are marking an aside. Name the plan which we were working on before as `[PLAN_A]` and write a new, subplan `[PLAN_B]` to temporarily switch to.
    - We will switch back to `[PLAN_A]` immediately after `[PLAN_B]` completion.
- `[LEARN]`: Review learnings and map them to documentation.
    - Some learnings may be outdated, so please ask me which lessons to forget.
    - Make surgical doc/spec updates of the learnings. Request edit permissions where required.
    - Empty the learnings table for next time.
    - Commit this work so we preserve learnings.
- `[MONITOR]`: A script is running and will output logs/progress/results which you need to await -> evaluate -> maybe intervene -> await -> ...
    - Spec alignment is first priority, do not drift away through iterations.
    - Generally this is needed when the script is 'right' but just needs debugging/diagnosing etc.
- `[DIAGNOSE]`: What is the underlying cause of this symptom?
    - No band-aid, hacky or workaround fixes
    - You may use agents for diagnostic experiments
    - We are experimentally driven, not speculative
    - Agentically consider high level (philosophy, underlying math, etc), medium level (integration, usage, etc) and low level (bugs, syntax, etc).
    - A `[DIAGNOSE]` output may be diagnosis-only, but must not be reported as a fix or closure.
- `[TERMINAL_CONDITION]`: Do not 'exit', 'return to user', 'apply `<|endoftext|>`' or similar unless `[TERMINAL_CONDITION]` is met.
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
- `[SPEC_REVIEW]`: Compare implementation to the specification (may be a subset of spec).
    - Check alignment agentically by type:
        - Logic
        - Implementation
        - Correctness
        - Documentation
        - Outputs
        - Defensibility
        - Laziness
    - Write each misalignment point into the `AI_SPACE/TODO.md`, in order of severity and grouped by issue.


# SPEC Usage
- Spec will have a walkthrough section with work stages/steps/milestones.
- Spec doc is generally the guide to build the project, not its usage, for example:
    - The steps to build a research suite, not the actual experiments.
    - The steps to build an app, not the actual app itself.
- The 'usage' comes later, and generally the spec is swapped out for an explicit 'implementation guide'.


# Learnings
- Update `AI_SPACE/AI_LEARNINGS_LOG.md` after:
    - failures
    - debugging discoveries
    - architecture/course corrections
    - mistakes
- Update `AI_SPACE/TODO.md` only with concrete unresolved follow-up work.
- Do not fill TODOs with vague ideas, duplicates or already-completed work.
- Always run the `[LEARN]` operation when updating learnings.
- Do not use TODO/learnings updates as a substitute for completing the requested implementation, proof, validation or spec-alignment work.


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


# Done Means
- The requested change exists in the repo state, not only in docs/plans/reports.
- The code change is complete, coherent and aligned with the spec or explicit human instruction.
- Relevant checks or real runs have been completed at the right stage.
- Exact validation commands/checks and pass results are reported.
- Config, docs and outputs have been updated where behaviour changed.
- Obsolete assumptions and replaced logic in touched areas have been cleaned up.
- Learnings, TODOs and handovers have been updated when relevant.
- Required spec alignment passes a `[SPEC_REVIEW]`.
- A plan's implementation is complete, with no gaps, no surprises, no laziness and no workarounds.
- There are no known in-scope gaps, placeholders, workarounds, cosmetic completions or silently deferred items.
- Remaining limitations or next steps are allowed only when:
    - they are outside the requested scope, or
    - they are explicitly approved human deferrals, or
    - the task is reported as `[BLOCKED]`, not `[DONE]`.
- If validation fails or cannot be run, Done Means is not satisfied unless the human explicitly requested no validation.
- The deliverable is the completed repo change plus validation evidence, not a plan, diagnosis, classification, note or documented gap.
- Do not stop after naming, documenting or categorising a shortfall. If the requested work is not complete, continue the work loop or report `[BLOCKED]`.
- `[DONE]` is allowed only when the requested work exists in the repo and the relevant validation has passed, or when the human explicitly requested analysis, diagnosis, planning or documentation only.
- `[Done]` during goal mode is normally a sub-task completion, not a real exit.
- `[BLOCKED]` is not completion. Use it only after a concrete implementation/validation attempt fails for a reason outside current authority, available tools or safe operating limits.
- Blocker reports must include:
    - exact command/check that failed or could not be run
    - exact error or missing authority/tooling
    - files changed
    - concrete attempts made
    - smallest next action needed from a human
- Forbidden completion substitutes:
    - "I have documented that ..."
    - "classified as ..."
    - "proof consolidation gap"
    - "the remaining work is ..."
    - "X helped only a little, but Y is still the real blocker"
    - TODO-only, note-only or documentation-only changes unless explicitly requested
- If a gap is found, close it. Do not preserve it as a named category.


## Final Report Contract
- For implementation, proof, debugging, refactoring and spec-alignment tasks, the final response must begin with either `[DONE]` or `[BLOCKED]`.
- `[DONE]` reports:
    - files changed
    - validation commands/checks run
    - pass result
    - behaviour/spec outcome
- `[BLOCKED]` reports:
    - exact failed/unavailable command or check
    - exact remaining error/blocker
    - concrete repair attempts already made
    - files changed
    - smallest next human decision/action needed
- Do not report `[DONE]` if validation failed, validation was skipped by choice, or the requested behaviour is still absent.
