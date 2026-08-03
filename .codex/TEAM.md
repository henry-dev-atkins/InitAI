# Codex Team Model

Use `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` to select the project-scoped `orchestrator` custom agent. The agent must load `$orchestrator` before campaign work.

`.codex/agents/orchestrator.toml` defines the manager identity and control-plane posture. `.agents/skills/orchestrator/SKILL.md` is the sole procedural workflow authority. Team profiles provide bounded capabilities; they do not add phases or control the portfolio.

## Roles

- `orchestrator`: project-scoped control-plane agent; owns findings, workstreams, state, assignment, locks, commits and completion; loads `$orchestrator`; never implements project code.
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

1. Maintain a campaign map of destination, durable outcomes, dependencies, planning horizons and fog; use `$spec-explore` when the route is not decision-complete.
2. Run evidence-backed spec review and use `$verify-finding` before promoting disputed or weakly evidenced claims.
3. Use `$plan-portfolio` to preserve several independent large outcomes rather than fragmenting one local issue across workers.
4. Maintain readiness queues for planning, review, implementation, validation and fog clearing.
5. Use `$portfolio-next` whenever capacity becomes free; phase order applies per workstream rather than globally.
6. Use `$plan-blastradius` for contract-changing plans and accepted diffs that may invalidate prepared work.
7. Run read-only implementation/integration review for every result and immediately release newly unblocked outcomes.
8. Use `$campain-review` at milestones, stalls or material evidence changes; repeat until terminal review succeeds on one frozen revision.

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

## Agent versus skill boundary

Use a custom agent when the repository needs a durable worker identity with a distinct context, sandbox or sceptical/implementation posture. Use a skill when the same current agent should follow a reusable procedure.

Keep these as custom agents backed by skills where relevant:

- `orchestrator` + `$orchestrator`: durable control plane plus orchestration procedure.
- `research-architect` + planning/spec skills: isolated read-only planning identity.
- `spec-reviewer` + `$spec-review`: independent sceptical spec-alignment identity.
- `diagnosis-agent` + `$diagnose`: isolated root-cause investigation identity.
- `merge-captain` + review/maintenance skills: independent implementation acceptance identity.
- implementation and validation agents + bounded execution skills: separate write scopes and runtime postures.

Keep portfolio, planning, review-lens, maintenance, session, prototype, monitoring and workflow-ontology items as skills. They are procedures or criteria that several agent identities may need; converting them into agents would duplicate authority and increase routing overhead.
