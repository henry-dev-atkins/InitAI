# AGENTS.md

The project authority is `AI_SPACE/SPEC.md` when present.

If `AI_SPACE/SPEC.md` is missing, use the explicit human prompt only when it supplies concrete project intent and acceptance criteria. Otherwise report `[BLOCKED]`; do not invent project intent.

# Global rules

- No sycophancy.
- No secrets in code, logs, configs, handovers or artefacts.
- No spec rewriting unless `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` is present.
- Raise spec/prompt conflict immediately and explicitly. Do not silently choose one authority over the other.
- Do not edit outside the working repository unless `[EXTERNAL_EDIT_ALLOWED]` is present.
- Do not destructively delete anything. Move removals to `archive/` so they leave the active tree but remain recoverable.
- Check files, paths, modules and commands before referencing them.
- No silent fallback behaviour, silent errors, unsupported behaviour or GPU-to-CPU fallback.
- No placeholder content as a deliverable. Template field markers are allowed only inside templates.
- No silent GPU to CPU fallback.
- No ad hoc output sprawl across the repository root.
- UK English spelling.
- Every new dependency requires justification in an accepted plan.
- No documentation-only substitute for implementation, proof, test or validation unless documentation-only work was explicitly requested.
- No gap taxonomy as a deliverable unless diagnosis/taxonomy was explicitly requested.
- No editing anything outside the working repo/folder unless given the `[EXTERNAL_EDIT_ALLOWED]` flag; even then: NO DESTRUCTIVE DELETIONS EVER.
- No legacy compatibility, alternate-track behaviour, band-aids or local-only workarounds unless the spec explicitly requires them.
- All code and validation must run from inside the repository sandbox.

The AI workspace is `AI_SPACE/`:

- `sessions/`: finding registers, workstream registers, plans, reviews, task packets, locks and results.
- `handovers/`: reproducible end-of-session context.
- `AI_LEARNINGS_LOG.md`: durable lessons and mistakes.
- `TODO.md`: concrete unresolved work aligned with the current finding/workstream registers.
- `archive/`: old, superseded or noisy material moved out of active project paths but retained for manual recovery.

Workflow artefacts under `AI_SPACE/` are control metadata, not product capability, unless the spec explicitly says otherwise. `archive/` is historical recovery storage: archived material is outside the active product tree and must not be imported, executed, configured or counted as current implementation.

# Action routing

Capitalised bracket keywords are human-facing actions. Lowercase hyphenated names refer to folders under `.agents/skills/`.

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
- `[SPEC.IMPLEMENT]` or `[SPEC_IMPLEMENT]` -> `$spec-implement`
- `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` -> `$spec-edit`
- `[WORK_TYPE]` or `[WORKFLOW_ONTOLOGY]` -> `$workflow-ontology`
- `[WORKFLOW_STRUCTURE]` -> `$workflow-structure`
- `[DONE]` / `[BLOCKED]` -> `$final-report`
- `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` -> `$orchestrator`

If skill invocation is unavailable, locate the matching `SKILL.md` recursively under `.agents/skills/` using its frontmatter `name`, then apply it directly.

# Orchestrator authority

When `$orchestrator` is active, `.agents/skills/orchestrator/SKILL.md` is the single process authority. Other skills supply bounded planning, review, diagnosis, maintenance and validation criteria; they do not add phases, control sequencing or redefine completion.

The core loop is:

1. Agentic repository-wide spec review produces findings.
2. The orchestrator collates findings into one register and independent workstreams.
3. Planning agents produce one plan per ready workstream.
4. Plan-review agents accept or reject each plan; rejected plans are revised before implementation.
5. Implementation agents execute accepted, independent workstreams.
6. Review agents accept implementations or return concrete findings.
7. The orchestrator updates the registers and repeats until the terminal condition passes.

Operating boundaries:

- The main thread is the control plane and does not implement project source code while orchestration is active.
- The main thread may inspect, validate, write orchestration artefacts under `AI_SPACE/`, review diffs and create the final local commit.
- Only the orchestrator changes finding/workstream state, chooses work, assigns agents, manages locks, commits and declares session completion.
- Workers handle one task packet and report facts. They do not plan the portfolio, start unapproved write agents, select future work or invoke the terminal condition.
- Use up to six agents concurrently when that many ready, independent tasks exist. Never split, duplicate or invent work to fill capacity.
- Parallelise ready independent work. Serialise dependencies, overlapping writes, contract conflicts, integration gates and GPU-heavy runs.
- One session uses one current checkout. Workers do not create/switch branches or worktrees, merge, rebase, stage or commit.
- A write packet requires one owner, exact write scope, affected contracts, acceptance checks and an accepted plan.
- A rejected plan returns to planning. A rejected implementation is `PLAN_FAILED`, not a repair request: close source-writing authority for that plan, create or reopen findings, diagnose the planning failure when cause is not already evidenced, and return through normal workstream planning with a new plan ID. Reviewer "next step" text is evidence only; it cannot authorise repair, retry, patch-up or continuation source-writing.
- A tooling/access failure before source edits may retry once. `[BLOCKED]` is reserved for unavailable authority, tooling, data or safe execution paths—not merely unfinished implementable work.
- Default commit policy: workers never commit; the orchestrator creates one final local commit after terminal review unless the human explicitly requests a different integration policy.

Required session structure:

```text
AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/
  session_board.md
  finding_register.md
  workstream_register.md
  locks.md
  workstream__WS001__short-name/
    plan.md
    plan_review.md
    task_packet.md
    result_packet.md
    implementation_review.md
```

# Work types

Every workstream and plan declares one Primary Work Type. Required tests, config updates and behaviour documentation may remain supporting changes inside the same coherent workstream; split only when there are genuinely independent durable outcomes.

- `CAPABILITY.RESEARCH`: spec-backed durable research behaviour.
- `CAPABILITY.PRODUCT`: spec-backed durable product/user behaviour.
- `EVIDENCE.VALIDATION`: durable reusable validation evidence.
- `FIX.ALIGNMENT`: durable root-cause correction to match the spec.
- `DEPENDENCY.LOCAL`: portable local/repository infrastructure required by implementation.
- `TEMPORARY.DIAGNOSTIC`: scratch probing/logging; never committed.
- `ENVIRONMENT.ADAPTATION`: isolated local/sandbox/platform adaptation.
- `WORKAROUND.QUARANTINED`: explicit temporary workaround; never capability progress.
- `FLUFF.DISPOSABLE`: one-off plots, dumps, screenshots or exploratory artefacts.
- `DOCS.MEMORY`: TODOs, learnings, handovers and durable documentation.
- `AGENT.WORKFLOW`: agent instructions, skills, rules and templates.
- `CLEANUP.HYGIENE`: organisation without behaviour change.
- `SPEC.EDIT`: spec change requiring explicit spec-edit authority.

Only `CAPABILITY.RESEARCH`, `CAPABILITY.PRODUCT` and qualifying `FIX.ALIGNMENT` work count as capability progress. Supporting work does not become capability progress merely because it is packaged with capability work.

`TEMPORARY.DIAGNOSTIC`, `FLUFF.DISPOSABLE`, unapproved `ENVIRONMENT.ADAPTATION` and `WORKAROUND.QUARANTINED` outputs must not remain in active project paths at terminal completion. Move anything retained for recovery to `archive/`. Record Work Type in the workstream and plan; commit messages use the repository's normal prefix policy.

# Planning and review requirements

Every durable plan must contain:

- workstream ID, source finding IDs and exact spec authority;
- one Primary Work Type;
- one coherent outcome;
- owner agent;
- exact write scope and off-limits scope;
- contracts changed and consumed;
- ordered implementation steps;
- behavioural acceptance commands and evidence;
- protected invariants and prohibited behaviour;
- result-packet contract;
- an explicit `Am I going in Circles?` self-check;
- an explicit `Is there a more elegant way of doing this?` self-check.

Every plan requires agentic `[PLAN.REVIEW]`. Review may invoke `plan-elegance`, `maintain-review`, `maintain-elegance`, `maintain-techdebt`, `maintain-despaghettify`, `maintain-declutter` and `peer-review` as bounded review lenses. These skills remain supporting reviewers; they do not create new workflow stages.

# Guidance

- Work top-down: major missing capabilities and incorrect core behaviour before minor cleanup.
- Prefer the largest coherent step that safely converges on the spec.
- Keep designs minimal and repository-fitting; avoid software sprawl, speculative abstractions and repeated wrapper layers.
- Fail loudly and preserve useful diagnostic evidence.
- Use real behavioural validation where practical; small checks are for diagnosis, not final proof.
- Keep experiment behaviour config-driven.
- Keep generated artefacts in intentional locations and large data/checkpoints out of commits unless repository policy requires them.
- Use one GPU-heavy run at a time unless explicitly authorised otherwise.
- Worker `[DONE]` means only that its packet completed. Session `[DONE]` requires the terminal condition.



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
    - A failed post-implementation check invalidates acceptance. It is not permission for an ad hoc patch; return the evidence through implementation review and replanning.
- When inside goal mode, a worker `[DONE]` means a small subtask is done, not the whole goal, so keep iterating.
- If an agent cannot be started or cannot write in the current checkout, terminate/restart it if possible; otherwise report `[BLOCKED]`. The orchestrator must not implement as a fallback.
- Do not let work loops become too reactive to small failures. Challenge the direction when iterating through many small changes.
- Record durable decisions, accepted plans, findings, validation evidence, unresolved work and reusable lessons. Do not log every prompt, transient thought or routine action.
- Do not create small helper methods that are referenced only once.
- Avoid spaghettification, tech debt and code explosions. Keep repo changes focused on core spec capabilities; surrounding software must earn its place by directly enabling, simplifying or validating those capabilities.
- Never ever make 'special case' edits for branches within the repo, unless a high level requirement needs it.
- Implementation failure is always planning failure.



# Learnings
- Apply `[LEARN]` when you:
    - Solve a problem,
    - Create a workaround,
    - Human tells you to-do/not-to-do something,
    - Terminology to look for:
        - "That was wrong",
        - "Next time I should",
        - "Instead I should have",
