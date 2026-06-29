# Codex Team Model

Use `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` to activate `$orchestrator`.

## Roles

- `orchestrator`: main control plane; does not normally implement.
- `research-architect`: read-only research/spec decomposition.
- `ml-researcher`: write-capable ML/research implementation.
- `product-engineer`: write-capable product/user workflow implementation.
- `repo-engineer`: write-capable repo/dependency/config work.
- `validation-engineer`: behavioural validation and evidence.
- `spec-reviewer`: read-only spec review.
- `diagnosis-agent`: root-cause diagnosis.
- `merge-captain`: merge/integration review.
- `agent-workflow-engineer`: AGENTS/skills/Codex workflow maintenance.

## Execution pattern

1. Orchestrator reads spec/TODO/learnings/handovers.
2. Orchestrator writes `session_board.md` and `locks.md`.
3. Orchestrator writes one task packet per independent work package.
4. Plan review passes before write agents start.
5. Workers use branches/worktrees and return result packets.
6. Spec reviewer and merge captain review worker branches.
7. Orchestrator merges serially, validates globally and reports `[DONE]` or `[BLOCKED]`.
