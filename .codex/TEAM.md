# Codex Team Model

Use `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` to activate `$orchestrator`.

`.agents/skills/orchestrator/SKILL.md` is the sole workflow authority. Team profiles provide bounded capabilities; they do not add phases or control the portfolio.

## Roles

- `orchestrator`: control plane; owns findings, workstreams, state, assignment, locks, commits and completion; never implements project code.
- `research-architect`: read-only planning/research analysis for an assigned workstream.
- `ml-researcher`: write-capable ML/research implementation for one accepted task packet.
- `product-engineer`: write-capable product/user-flow implementation for one accepted task packet.
- `repo-engineer`: write-capable repository/dependency/config implementation for one accepted task packet.
- `validation-engineer`: behavioural validation; writes only when a task packet explicitly assigns validation files.
- `spec-reviewer`: read-only spec or implementation reviewer with an assigned lens.
- `diagnosis-agent`: read-only root-cause evidence gathering.
- `merge-captain`: read-only implementation/integration reviewer of the shared checkout.
- `agent-workflow-engineer`: write-capable AGENTS/skills/Codex workflow maintenance for one accepted task packet.

## Core execution pattern

1. Run an agentic whole-repository spec-review batch.
2. Orchestrator collates findings into one register and independent workstreams.
3. Planning agents produce one plan per ready workstream.
4. Plan-review agents accept or reject; rejected plans are revised before implementation.
5. Launch up to six accepted, mutually independent implementation workstreams.
6. Run read-only implementation/integration review for every result.
7. Accepted work resolves evidenced findings; rejected work creates/reopens findings and returns to planning.
8. Repeat until no open finding remains, global validation passes and terminal review succeeds.

## Concurrency and checkout

- Use up to six agents when that many ready independent tasks exist; never manufacture work to fill slots.
- All subagents use the current top-level checkout.
- Write agents receive disjoint write scopes with no contract conflicts.
- Overlapping/dependent work and GPU-heavy validation are serialised.
- Workers do not create/switch branches or worktrees, merge, rebase, stage or commit.
- The orchestrator creates the final local commit after terminal review unless the human explicitly requests another commit policy.

## Failure boundary

- Tool/access failure before edits may retry once.
- Plan rejection returns to replanning.
- Implementation rejection creates/reopens findings and returns through the normal workstream loop.
- Agents report evidence only; the orchestrator decides state transitions and future work.
- `[BLOCKED]` is for genuinely unavailable authority, tooling, data or safe execution—not unfinished implementable work.
