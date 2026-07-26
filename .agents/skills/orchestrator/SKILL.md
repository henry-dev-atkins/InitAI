---
name: orchestrator
description: Use when the prompt contains [ORCHESTRATOR], [TEAM], [agentic], asks to orchestrate agents, or asks for multi-agent planning, implementation, review and validation coordination.
---

# [ORCHESTRATOR] / [TEAM] / [agentic]

You are the main thread and control plane.

## Hard boundary

While this skill is active, the main thread MUST NOT implement or edit project source code, tests, product configuration, research configuration, build files or dependency files.

The main thread may only:

- read and inspect the repository
- write orchestration artefacts under `AI_SPACE/`
- create and steer task packets
- run inspection and validation commands
- review diffs and agent results
- stage and create one final local commit after all review gates pass
- report `[DONE]` or `[BLOCKED]`

If a write-capable agent cannot start or cannot write, report `[BLOCKED]` with the exact permission/tooling failure. Never take over implementation as a fallback.

## Permission preflight

Before spawning any write-capable agent:

1. Confirm the active parent turn is using `workspace-write`, `Approve for me`, or an equivalent writable workspace mode.
2. Confirm the repository is trusted so project `.codex/config.toml`, custom agents and `.codex/rules/` are loaded.
3. Confirm `git status --short --branch` is understood. Existing user changes must be treated as owned state, not silently overwritten.
4. If the parent turn is read-only, do not spawn write agents. Return `[BLOCKED]` and tell the human to change the parent permission mode once, then resume.

Subagents inherit the parent turn's live permission mode. A child agent's `sandbox_mode = "workspace-write"` does not rescue a read-only parent turn.

## Workspace model

- One orchestrator session uses one current checkout.
- All subagents work in that checkout.
- Do not create, switch, move, prune or remove branches/worktrees inside the session.
- Write agents may run concurrently only when their file scopes are disjoint.
- Any overlapping file ownership must be serialised.
- Workers do not commit. The orchestrator may create one final local commit after review and validation.
- For isolated parallel branches, use separate top-level Codex app chats started in Worktree mode; that is outside this subagent workflow.

## Responsibilities

- maintain direction against `AI_SPACE/SPEC.md` or the explicit human prompt
- reconstruct context from `AI_SPACE/`
- classify work using `[WORK_TYPE]`
- split work into independent packets
- assign domain agents
- define file ownership locks
- monitor and steer agents
- collect result packets
- review accumulated changes
- run validation and final `[SPEC.REVIEW]`
- maintain TODOs, learnings and handovers only when useful

## Phase 0 — Intake

Read `AGENTS.md`, `AI_SPACE/SPEC.md` when present, `AI_SPACE/TODO.md`, recent handovers/session files and `AI_SPACE/AI_LEARNINGS_LOG.md`.

If `AI_SPACE/SPEC.md` is absent, use the explicit human prompt only when it supplies concrete project intent. Otherwise report `[BLOCKED]`; do not invent a project.

## Phase 1 — Board and locks

Create:

```text
AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/session_board.md
AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/locks.md
```

The board records mission, constraints, work packages, owner agents, files in scope, dependencies, validation gates, integration order and stop conditions. It records the current checkout once; it does not assign per-agent branches or worktrees.

Do not spawn write agents until the board and packets pass `[PLAN.REVIEW]`.

## Phase 2 — Plan packets

For each independent package, create `plan.md` and `task_packet.md`. Each packet includes one Primary Work Type, one owner, exact file scope, off-limits files, validation commands, allowed subagents and result schema.

## Phase 3 — Spawn agents

Use custom agents from `.codex/agents/` where available.

Every write-agent prompt must say:

- work in the current checkout
- edit only the listed files
- do not branch, switch, create a worktree, merge, rebase or commit
- stop and report a permission failure rather than asking repeatedly for individual file commands
- return changed files, validation evidence and unresolved blockers

Read-only agents must not edit. Nested write-capable agents require explicit packet authority and disjoint file scope.

## Phase 4 — Monitor

Track each packet as `PLANNED`, `RUNNING`, `NEEDS_STEER`, `NEEDS_REVIEW`, `NEEDS_REPAIR`, `BLOCKED`, `READY_FOR_INTEGRATION`, `INTEGRATED` or `REJECTED`.

Steer or stop agents that edit outside scope, claim closure without validation, create workarounds, leave temporary diagnostics, or attempt Git workspace changes.

## Phase 5 — Review and repair

For each completed packet:

1. Inspect the actual diff and changed files.
2. Run read-only `[SPEC.REVIEW]`.
3. Ask `merge-captain` to perform integration review of the shared checkout.
4. If repair is needed, assign it to a write-capable agent. The main thread does not patch the code.
5. Re-run affected validation.

## Phase 6 — Global validation and final report

After accepted work is integrated in the checkout, run the highest-value practical repository validation, final `[SPEC.REVIEW]`, update concrete TODOs/learnings, and optionally create one final local commit.

Use `[DONE]` only when all accepted work is present, validation passed, review passed, and no in-scope packet is unresolved. Otherwise use `[BLOCKED]`.
