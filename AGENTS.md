# AGENTS.md

The project spec is `AI_SPACE/SPEC.md` when present.

If `AI_SPACE/SPEC.md` is missing, use the explicit human prompt only when it supplies concrete project intent and acceptance criteria. Otherwise report `[BLOCKED]`; do not invent project intent.

# Rules
- No sycophancy.
- No secrets in code.
- No secrets in logs, configs, handovers or artefacts.
- No spec rewriting unless `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` is present.
- SPEC misalignment must be IMMEDIATELY raised with maximum verbosity and significance.
    - If a human/prompt drifts from the spec, highlight it and clarify whether this was intentional. Humans make mistakes, but also change their mind: find out which.
    - Raising misalignment is not the same as finishing the task. After raising it, either continue once alignment is clear or report `[BLOCKED]`.
- Any operations outside the main folder/repo require detailed reports on why they are needed.
- Never delete any file/folder: all file/folder removals are moves to an `archive/` folder.
- No invented files, paths, modules or commands: check first, then reference.
- No silent fallback behaviour.
- No placeholder content as a deliverable. Template field markers are allowed only inside templates.
- No silent GPU to CPU fallback.
- No ad hoc output sprawl across the repo root.
- No silent errors or quietly unsupported behaviour.
- UK English spelling, not US English.
- No editing anything outside the working repo/folder unless given the `[EXTERNAL_EDIT_ALLOWED]` flag; even then: NO DELETIONS EVER.
- Every new dependency needs justification.
- No documentation-only substitutions for implementation, proof, test or validation work unless documentation-only work was explicitly requested.
- No gap classification or issue taxonomy as a deliverable unless the human explicitly requested diagnosis/taxonomy only.
- Forbidden terminology and phrasing in reports, plans, invented architecture names or task outcomes:
    - Canonic (ise/al)
    - Canonical
    - Version X
    - Word soup. Use direct language instead.
    - Placeholder
    - Honest
    - Documented gap
    - Classified gap
    - Proof consolidation gap
- The AI workspace is `AI_SPACE/`, with:
    - `sessions/` for session boards, plans, task packets, locks and result packets.
    - `handovers/` for reproducible end-of-session context dumps.
    - `AI_LEARNINGS_LOG.md` for lessons, mistakes and vital information discovered through work.
    - `TODO.md` for concrete unresolved tasks, aligned with `sessions/` and current progress.
    - `archive/` for old/noisy material that must not be deleted.
- If `agentic`, `[agentic]`, `[TEAM]` or `[ORCHESTRATOR]` is requested, use `$orchestrator` and subagents for independent exploration, review, diagnosis, implementation and merge review.
- All code must run from inside the sandbox/repo, no external runs.

# Action routing

Capitalised bracket keywords are the human-facing action language. Keep them visible in prompts, plans, reports and skill headings. Use lowercase hyphenated Codex skill names and matching folder names under `.agents/skills/`.

- `[SESSION.START]` -> `$session-start`
- `[SESSION.CLEAN]` -> `$session-clean`
- `[SESSION.END]` -> `$session-end`
- `[PLAN]` -> `$plan`
- `[PLAN.REVIEW]` or `[PLAN_REVIEW]` -> `$plan-review`
- `[PLAN.SUB]` or `[SUBPLAN]` -> `$plan-sub`
- `[PLAN.TERMINAL_CONDITION]` or `[TERMINAL_CONDITION]` -> `$terminal-condition`
- `[LEARN]` -> `$learn`
- `[MONITOR]` -> `$monitor`
- `[DIAGNOSE]` -> `$diagnose`
- `[SPEC.REVIEW]` or `[SPEC_REVIEW]` -> `$spec-review`
- `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` -> `$spec-edit`
- `[WORK_TYPE]` or `[WORKFLOW_ONTOLOGY]` -> `$work-type`
- `[WORKFLOW_STRUCTURE]` -> `$workflow-structure`
- `[DONE]` / `[BLOCKED]` final reports -> `$final-report`
- `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` -> `$orchestrator`

If a capitalised trigger is present and skill support is available, invoke the mapped `$skill-name`. If skill invocation is unavailable, apply the corresponding `.agents/skills/<skill-name>/SKILL.md` workflow directly.

All `[PLAN]`, `[PLAN.REVIEW]`, `[PLAN.SUB]`, `[PLAN.TERMINAL_CONDITION]`, `[SPEC.REVIEW]` and `[ORCHESTRATOR]` workflows must apply `[WORK_TYPE]`.

# Team / orchestrator operating model

When `$orchestrator` is active:

- The main thread is the control plane. It MUST NOT implement or edit project code while `$orchestrator` is active.
- The main thread may write only orchestration artefacts under `AI_SPACE/`, run inspection/validation, review diffs, and create one final local commit after review.
- If a write-capable agent cannot start or write, report `[BLOCKED]`; the main thread must not take over implementation.
- The main thread owns direction, context, plan quality, dependency graph, file ownership, integration order, validation gates and final reporting.
- Domain agents own bounded work packages.
- Subagents are used for read-only exploration, diagnosis, review and validation critique by default.
- Nested write-capable subagents require explicit task-packet authority.
- One orchestrator session uses one current checkout. Do not create or switch branches/worktrees inside the subagent workflow.
- One durable write plan has one owner agent and an exact file scope.
- Two write-capable agents must not own the same files unless the orchestrator serialises the work.
- Workers do not stage or commit; the orchestrator may create one final local commit after all gates pass.
- Worker `[DONE]` means the worker packet is complete, not that the whole session is complete.
- Session `[DONE]` requires orchestrator review, accepted integration state in the current checkout, validation and final `[SPEC.REVIEW]`.
- Integrate and review write packages serially when their file scopes overlap, even if independent work happened in parallel.
- Schedule GPU-heavy runs serially unless the human explicitly authorises parallel GPU contention.

Required orchestrator artefacts live under:

```text
AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/
  session_board.md
  locks.md
  plan__P001__short-name/
    plan.md
    task_packet.md
    result_packet.md
```

# Types of work

Every plan must declare exactly one Primary Work Type. A plan may contain supporting work only when it is explicitly labelled as a subplan, temporary diagnostic step, cleanup step or validation step. If work has more than one durable purpose, split it into separate plans.

Primary Work Types:

- `CAPABILITY.RESEARCH`: spec-backed durable research behaviour. Commit required. Counts as capability progress.
- `CAPABILITY.PRODUCT`: spec-backed durable product/user behaviour. Commit required. Counts as capability progress.
- `EVIDENCE.VALIDATION`: durable validation evidence. Commit reusable/lightweight evidence only. Does not itself count as capability progress.
- `FIX.ALIGNMENT`: durable root-cause correction to match spec or prompt. Commit required. Counts as capability progress only when it restores/unlocks a capability.
- `DEPENDENCY.LOCAL`: portable local/repo infrastructure needed for work. Commit only if reusable and justified. Does not count as capability progress.
- `TEMPORARY.DIAGNOSTIC`: scratch debugging/probing/logging. Do not commit. Must be removed or archived before `[DONE]`.
- `ENVIRONMENT.ADAPTATION`: isolated local/sandbox/platform adaptation. Do not commit unless explicitly approved. Must not alter core behaviour.
- `WORKAROUND.QUARANTINED`: explicit workaround for a local/sandbox/platform constraint. Do not commit by default. Never use to claim capability progress.
- `FLUFF.DISPOSABLE`: one-off plots, dumps, screenshots or exploratory artefacts. Do not commit. Archive or remove.
- `DOCS.MEMORY`: docs, TODOs, learnings, handovers and project memory. Commit when useful/requested. Does not substitute for implementation.
- `AGENT.WORKFLOW`: durable agent tooling/instructions such as `AGENTS.md`, `.agents/skills/`, `.codex/agents/`, `.codex/rules/` and prompt templates. Commit when useful/requested. Does not count as capability progress.
- `CLEANUP.HYGIENE`: repo organisation without behaviour change. Commit if durable.
- `SPEC.EDIT`: spec change. Requires `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]`. Commit with `SPEC_EDIT:`.

Work Type Rules:

- Only `CAPABILITY.RESEARCH` and `CAPABILITY.PRODUCT` count as capability progress.
- A capability plan cannot close as `[DONE]` if its durable changes are only docs, cleanup, dependency work, agent workflow work, temporary diagnostics, environment adaptation, workaround or fluff.
- `TEMPORARY.DIAGNOSTIC`, `FLUFF.DISPOSABLE`, unapproved `ENVIRONMENT.ADAPTATION` and `WORKAROUND.QUARANTINED` work must not be committed.
- `DEPENDENCY.LOCAL`, `DOCS.MEMORY`, `AGENT.WORKFLOW`, `CLEANUP.HYGIENE`, `EVIDENCE.VALIDATION` and `SPEC.EDIT` may be committed when durable and justified, but they do not count as capability progress.
- If the agent cannot classify work into one Primary Work Type, split the work or report `[BLOCKED]` with the ambiguity.
- Work Type must be present in every commit message. 

# Guide

- Favour simplicity - no overengineering.
- Fail fast, frequently and with maximum explainability - learn from mistakes in `AI_SPACE/AI_LEARNINGS_LOG.md`.
- We have access to one GPU locally (RTX 5090).
- Config driven research means that implementing new classes etc should be easy.
- Keep it Simple, Stupid!
- Keep temporary files (`.ruff_cache/`, `.triton_tmp/`) inside `temp/` to minimise clutter.
- Do not use fake or toy validation as closure for real research behaviour.
    - Intermediate diagnostic checks may be small when they isolate a failure.
    - End-of-plan validation should use real runs where practical.
- Test only valuable, behavioural logic, not basic stuff.
- GPUs for ML, not CPU.
- Unsupported GPU, CUDA or device situations must fail loudly and clearly.
- Call out expected performance, VRAM or RAM impact when it is materially affected.
- The best tests and correctness checks are real runs, and should be done at the end of plans where practical.
    - MNIST CNN 100 epochs, not a small simulated dataset - at the end.
    - Analysis library correctly plots real runs, not fake simulated runs.
    - MNIST CNN 5 epochs, not a small simulated dataset - at intermediate development steps/checks.
- Never support legacy work.
    - We are current state only.
    - In the case of a change, change the code, do not wrap old logic.
    - Do not support or maintain legacy logic or backwards compatibility.
    - No band-aids: implement the actual change.
    - Only current-state work, no alternate-track work.
- Config should be the source of truth for experiment behaviour.
- Avoid hardcoded experiment values when config should own them.
- New features should slot cleanly into the config structure.
- Generated artefacts should go to clear, intentional output locations.
- Large datasets and checkpoints should follow repo storage conventions and must not be casually committed.
- Git commits should start with `CLEANUP:`, `FEAT:`, `CONFIG:`, `DOCS:`, `FIX:`, `TEST:`, `AI:` or `SPEC_EDIT:`.
- Prefer repo-standard tools and commands over ad hoc alternatives.
- Efficiently design entry points to minimise permission/approval delays. Subagents inherit the parent turn permission mode, so confirm the parent is writable before spawning write agents.
- For allow-listed safe inspection commands, announce with `***` and proceed without asking for permission. Prefer stable commands such as `rg`, `rg --files`, `Get-Content`, `Get-ChildItem`, and `Select-String`; avoid aliases such as `cat`, `grep`, `find`, and `ls` in durable guidance, and avoid PowerShell pipelines for routine inspection.
- No workarounds as deliverables.
    - No stubs.
    - No named shortfalls as deliverables.
    - No laziness.
    - No cosmetic completion.
    - A failing command/check is the next repair target, not an endpoint.
- When inside goal mode, a worker `[DONE]` means a small subtask is done, not the whole goal, so keep iterating.
- If an agent cannot be started or cannot write in the current checkout, terminate/restart it if possible; otherwise report `[BLOCKED]`. The orchestrator must not implement as a fallback.
- Do not let work loops become too reactive to small failures. Challenge the direction when iterating through many small changes.
- All plans, prompts, heuristics, rules of thumb and things of note must be documented/logged/tracked in `AI_SPACE/` or the repo itself.
- Do not create small helper methods that are referenced only once.
- Avoid spaghettification, tech debt and code explosions. Keep repo changes focused on core spec capabilities; surrounding software must earn its place by directly enabling, simplifying or validating those capabilities.
- Never ever make 'special case' edits for branches within the repo, unless a high level requirement needs it.

# SPEC usage

- Spec will have a walkthrough section with work stages/steps/milestones.
- Spec doc is generally the guide to build the project, not its usage.
- The usage comes later, and generally the spec is swapped out for an explicit implementation guide.

# Learnings
- Apply `[LEARN]` when you:
    - Solve a problem,
    - Create a workaround,
    - Human tells you to-do/not-to-do something,
    - Terminology to look for:
        - "That was wrong",
        - "Next time I should",
        - "Instead I should have",



# Plans

- Planning should be done considering all layers of the project. Get as much documentation and code into context as possible to minimise errors.
- Every plan must include a `Work Classification` block from `$work-type`.
- Every durable write plan must include owner, exact file scope, validation gate and integration order.
- All plans must consider consequences, for example:
    - If a variable changes type, where is it used?
    - Do we still assume the old type anywhere?
- All plans require explicit, agentic plan reviews for:
    - Overengineering
    - Minimalism - the smallest coherent repo change that directly advances the requested outcome
    - Technical debt
    - Redundant iterations
    - More elegant implementation missed
    - True implementation of the intended framework
    - Regression to non-correct implementation
    - Gaps, ambiguity or contradictions
    - Work Type classification quality
    - File ownership and orchestration safety
- Plans guide execution; plans are not deliverables unless the human explicitly requested plan-only output.
- Plan reviews must feed back into implementation. Do not stop at "plan reviewed".
- Plans must state assumptions, key tradeoffs, unresolved risks and follow-up work.
- Final reports may state follow-up work only after `[DONE]`, `[BLOCKED]`, or human-approved deferral. Follow-up work is not closure.
- All plans should end in a short, human-facing executive summary of the work. The summary is not a terminal condition.
- Every plan must include a section headed `AM I GOING IN CIRCLES?` with a direct yes/no answer, the reason, and the stop/pivot condition if the work starts repeating without new evidence.
- Plans are reviewed bottom up by humans scrolling up through the terminal, not top down.
- If a plan implementation will/does end with "X helped only a little, but Y is still the real blocker", it is a planning/diagnosis failure: stop, re-run `[DIAGNOSE]`, and re-plan before implementing more.
