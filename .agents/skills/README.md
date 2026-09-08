# Skill map

The orchestrator loop has six core skills. Every other installed skill is an optional bounded tool. Optional skills do not create workflow phases or own future-work decisions.

## Core loop

- `$orchestrator`: Run the project-scoped spec-convergence loop.
- `$conformance`: Compare `AI_SPACE/SPEC.md` with the repository and return material findings or `PASS`.
- `$outcome-decomposition`: Group current findings into independent durable workstreams.
- `$select-ready-work`: Select the next useful ready independent workstreams.
- `$plan`: Create one implementation-ready plan for one selected workstream.
- `$plan-review`: Independently accept, reject, or block one workstream plan.

## Planning and review tools

- `$change-impact-analysis`: Trace downstream effects of shared interface, schema, config, or behaviour changes.
- `$first-principles`: Challenge assumptions and reason from the underlying problem.
- `$parallel-safety`: Check accepted plans for safe parallel execution.
- `$peer-review`: Review repository defensibility and reproducibility.
- `$plan-desk-check`: Simulate one plan before implementation begins.
- `$plan-elegance`: Review whether a plan is the simplest coherent solution.
- `$plan-preflight`: Check mechanical plan completeness before semantic review.
- `$plan-sub`: Break one accepted plan step into local execution substeps.
- `$strategy-review`: Reframe the current approach after repeated failure or no progress.
- `$procedural-task-entry-points`: Keep concrete task control flow procedural.

## Specification tools

- `$requirements-discovery`: Explore unclear requirements or repository evidence before conformance review or planning.
- `$finding-verification`: Independently verify one disputed or weakly evidenced conformance finding.
- `$spec-edit`: Apply an explicitly authorised minimal edit to `AI_SPACE/SPEC.md`.

## Implementation and diagnostic tools

- `$adversarial-review`: Challenge a non-trivial decision with a fresh-context critic.
- `$ask-first`: Clarify the request before planning or implementation when the user asks for that mode.
- `$bounded-execution`: Keep long or stateful agent work bounded, checked, and resumable.
- `$comprehensive-testing`: Design or review practical multi-layer test coverage.
- `$diagnose`: Find the underlying cause of a failure or unexplained behaviour.
- `$done`: Check completion and produce `[DONE]` or `[BLOCKED]` evidence.
- `$implementation-desk-check`: Trace implementation behaviour without running the target behaviour.
- `$simplified-technical-english`: Rewrite agent-facing English to reduce ambiguity.
- `$test-driven-development`: Drive behaviour changes with failing and passing tests.
- `$vertical-slicing`: Build multi-file work in small validated vertical slices.
- `$workflow-ontology`: Classify repository work by project workflow type.
- `$workflow-structure`: Define the minimal resumable `AI_SPACE` session layout.

## Maintenance, learning, session, and style tools

- `$learn`: Record durable lessons and unresolved follow-up work.
- `$retro`: Review process quality, progress rate, efficiency, and orchestration behaviour.
- `$progress-report`: Write a quantitative report for one orchestration session.
- `$maintain-declutter`: Audit repository files for commit, archive, move, or human-review decisions.
- `$thorough-removal`: Remove obsolete repository paths and their orphaned consequences.
- `$maintain-despaghettify`: Review tangled structure, coupling, and dependency spread.
- `$maintain-elegance`: Review repository-wide simplicity, coherence, and capability fit.
- `$maintain-review`: Review drift away from the spec and core capabilities.
- `$maintain-techdebt`: Review technical debt and future maintenance cost.
- `$maintain-terminology`: Check resources for accepted project terminology and prohibited ideas.
- `$session-clean`: Consolidate session clutter without deleting durable evidence.
- `$session-compact`: Compact session state while preserving resumability.
- `$session-end`: Write a reproducible end-of-session handover.
- `$session-start`: Start a minimal resumable orchestration session.
- `$code-style`: Apply the repository coding style.
- `$henrys-voice`: Draft free text in Henry Atkins's analytical technical voice.

## Discovery

If skill invocation is unavailable, locate the matching `SKILL.md` recursively under `.agents/skills/` using its frontmatter `name`.
