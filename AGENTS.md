# AGENTS.md
Our spec is at `AI_SPACE/SPEC.md`. If it is not present, please throw an error.

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
    - `sessions/` store every session->plan->subplan->... you generate (timestamp in name)
    - `handovers/` context dump of the work for tomorrow
    - `AI_LEARNINGS_LOG.md` store lessons, mistakes and vital information you pick up through work. Keep it clean.
    - `TODO.md` is a rolling store of tasks (live task list) that you add to, align with `sessions/` and use for progress tracking. Do not delete elements unless perfectly implemented.
- If 'agentic' is requested, use `$orchestrator` and subagents for independent exploration, review, diagnosis, or plan critique.
- All code must run from inside your sandbox/repo, no 'external' runs.


# Action routing
Capitalised bracket keywords are the human-facing action language. Keep them visible in prompts, plans, reports and skill headings. Use lowercase hyphenated Codex skill names and matching folder names under `.agents/skills/`.

- `[SESSION.START]` -> `$session-start`
- `[SESSION.CLEAN]` -> `$session-clean`
- `[SESSION.END]` -> `$session-end`
- `[PLAN]` -> `$plan`
- `[PLAN.REVIEW]` -> `$plan-review`
- `[PLAN.SUB]` -> `$plan-sub`
- `[PLAN.TERMINAL_CONDITION]` -> `$plan-terminal-condition`
- `[LEARN]` -> `$learn`
- `[MONITOR]` -> `$monitor`
- `[DIAGNOSE]` -> `$diagnose`
- `[SPEC.REVIEW]` -> `$spec-review`
- `[SPEC.EDIT_REQUIRED]` -> `$spec-edit`
- `[DONE]` / `[BLOCKED]` final reports -> `$final-report`
- `[agentic]` or `[ORCHESTRATOR]` -> `$orchestrator`
- `[WORKFLOW_STRUCTURE]` -> `$workflow-structure`

If a capitalised trigger is present and skill support is available, invoke the mapped `$skill-name`. If skill invocation is unavailable, apply the corresponding `.agents/skills/<skill-name>/SKILL.md` workflow directly.


# Guide:
- Favour simplicity - no overengineering
- Fail fast, frequently and with maximum explainability - learn from mistakes in `AI_SPACE/AI_LEARNINGS_LOG.md`
- We have access to one GPU locally (RTX 5090)
- Config driven research means that implementing new classes etc should be easy
- Keep it Simple, Stupid!
- Keep temporary files (`.ruff_cache/`, `.triton_tmp/`) inside `temp/` to minimise clutter
- No smoke tests, minimal dry runs in the main codebase - we are a research project not a software company
    - Use the `temp/` file for any intermediate/dev work that is needed
    - Do not use fake or toy validation as closure for real research behaviour.
    - Intermediate diagnostic checks may be small when they isolate a failure.
    - End-of-plan validation should use real runs where practical.
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
- If agent cannot be started, please terminate the agent if it is running and restart, if you cannot do that, error for human intervention.
- Do not let work loops became too reactive to small failures - ensure you're challenging the direction when iterating through many small changes.



# SPEC Usage
- Spec will have a walkthrough section with work stages/steps/milestones.
- Spec doc is generally the guide to build the project, not its usage, for example:
    - The steps to build a research suite, not the actual experiments.
    - The steps to build an app, not the actual app itself.
- The 'usage' comes later, and generally the spec is swapped out for an explicit 'implementation guide'.