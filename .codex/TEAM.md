# Codex Team Model

Use `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` to activate `$orchestrator`.

## Roles

- `orchestrator`: main control plane; never implements project code while orchestration is active.
- `research-architect`: read-only research/spec decomposition.
- `ml-researcher`: write-capable ML/research implementation.
- `product-engineer`: write-capable product/user workflow implementation.
- `repo-engineer`: write-capable repo/dependency/config work.
- `validation-engineer`: behavioural validation and evidence.
- `spec-reviewer`: read-only spec review.
- `diagnosis-agent`: root-cause diagnosis.
- `merge-captain`: integration review of the shared session checkout.
- `agent-workflow-engineer`: AGENTS/skills/Codex workflow maintenance.

## Execution pattern

1. The orchestrator reads the spec, TODO, learnings and recent handovers.
2. The orchestrator confirms the parent chat is in `workspace-write` or `Approve for me` mode before spawning write agents.
3. The orchestrator writes `session_board.md`, `locks.md`, and one task packet per independent work package.
4. Plan review passes before write agents start.
5. All subagents work in the current session checkout. Write agents receive disjoint file ownership; overlapping work is serialised.
6. Workers do not create branches, switch branches, create worktrees, merge or commit.
7. Spec review and integration review inspect the accumulated checkout.
8. The orchestrator runs global validation and may create one final local commit after review.
9. If a write-capable agent cannot write, the orchestrator reports `[BLOCKED]`; it must not take over implementation.

## Worktree boundary

A Codex app worktree belongs to the top-level chat. Subagents inside that chat use its current checkout. For truly isolated parallel branches, start separate top-level chats in separate app worktrees; do not create nested worktrees from the orchestrator workflow.
