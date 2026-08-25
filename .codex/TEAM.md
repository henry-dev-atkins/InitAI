# Codex Team Model

Use `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` to select the project-scoped `orchestrator` custom agent. The agent loads `$orchestrator` before campaign work.

`.codex/agents/orchestrator.toml` defines the manager identity. `.agents/skills/orchestrator/SKILL.md` defines the loop.

## Roles

- `orchestrator`: owns misalignments, workstreams, selection, assignments, verdicts and completion. It never implements project source code.
- `spec-reviewer`: read-only spec alignment review.
- `research-architect`: read-only planning for one selected workstream.
- `ml-researcher`: ML/research implementation for one accepted plan.
- `product-engineer`: product/user-flow implementation for one accepted plan.
- `repo-engineer`: repository/config/dependency implementation for one accepted plan.
- `agent-workflow-engineer`: AGENTS/skills/Codex workflow implementation for one accepted plan.
- `validation-engineer`: bounded behavioural validation. It writes only when the accepted plan includes validation files.
- `merge-captain`: read-only implementation acceptance reviewer.
- `diagnosis-agent`: read-only root-cause investigation.

## Core execution pattern

1. `$spec-review` returns material misalignments or `PASS`.
2. `$plan-portfolio` collates misalignments into independent durable workstreams.
3. `$portfolio-next` selects the next N useful ready workstreams.
4. One planning agent creates one `$plan` for each selected workstream.
5. One independent reviewer runs `$plan-review` for each plan. Rejected plans return to planning.
6. Accepted plans run in parallel when their write scopes and important dependencies are independent.
7. `merge-captain` reviews each implementation and returns `ACCEPT_IMPLEMENTATION`, `REJECT_IMPLEMENTATION`, or `BLOCKED`.
8. Rejected implementation returns to planning. Implementation failure is always planning failure.
9. After the batch, return to `$spec-review`.
10. Stop only when the new spec review is clean.

## Concurrency and checkout

- Use up to six agents when that many useful independent tasks exist.
- All subagents use the current top-level checkout.
- Parallel write agents need independent accepted write scopes.
- Serialise overlapping work and important shared resources.
- Workers do not create/switch branches or worktrees, merge, rebase, stage or commit.

## Skills

Core loop skills control workflow order. Other skills remain available as optional bounded tools. Supporting skills cannot create new workflow stages, change accepted scope, or choose future work.
