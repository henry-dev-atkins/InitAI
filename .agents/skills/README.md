# Skill map

The orchestrator loop has six core skills. Every other skill remains available as an optional bounded tool. Optional skills do not create workflow phases or own future-work decisions.

## Core loop

- `$orchestrator`: Procedural workflow for the project-scoped orchestrator custom agent. Use to repeatedly review the repository against AI_SPACE/SPEC.md, turn misalignments into independent workstreams, plan and review them, implement accepted plans, review the work, and repeat until spec review is clean.
- `$plan`: Create one implementation-ready plan for one selected workstream. The plan fixes WHAT is authorised while leaving the implementation agent freedom over HOW to execute it safely.
- `$plan-portfolio`: Collate the current spec-review misalignments into coherent independent durable workstreams. Output the workstream list only; do not plan implementation details.
- `$plan-review`: Independently review one workstream plan for spec alignment, completeness, scope, validation and implementation clarity. Return ACCEPT, REJECT or BLOCKED.
- `$portfolio-next`: Select the next N useful ready independent workstreams from the current workstream list for planning or implementation.
- `$spec-review`: Compare AI_SPACE/SPEC.md with the current repository and return an exhaustive list of material misalignments, or PASS when none remain. This is the outer convergence test for the orchestrator loop.
- `$code-style`: Code style guide.

## Optional control and utility skills

- `$campain-review`: Optional back-to-basics review when repeated plan or implementation failures suggest the current workstream split or direction is wrong.
- `$plan-blastradius`: Optional impact check for a plan or accepted implementation that changes a shared interface, schema, config contract or other widely consumed behaviour.
- `$plan-parallel-collate`: Optional safety check for a set of accepted plans before parallel implementation. Use only when parallel independence is not obvious.
- `$plan-preflight`: Optional quick mechanical completeness check for one plan before semantic plan review.
- `$session-clean`: Use when the prompt contains [SESSION.CLEAN], or when repo clutter, handovers, plans, session boards, TODOs, learnings, temporary artefacts or agent outputs need consolidation without deleting files.
- `$session-compact`: Compact a long AI_SPACE session by preserving accepted plans/reviews and replacing noisy transient notes with one short current-state summary.
- `$session-end`: End an orchestration session with a short handover containing the current outer-loop state and unresolved work.
- `$session-start`: Start one lightweight orchestration session and create only the minimal durable files needed to resume the simple convergence loop.
- `$spec-edit`: Use only when the prompt contains [SPEC.EDIT_REQUIRED] or [SPEC EDIT REQUIRED]. Plan, review, and apply a minimal edit to AI_SPACE/SPEC.md, then review downstream consequences.
- `$spec-explore`: Optional read-only exploration used when the spec or repository area is not yet clear enough for a confident spec review or plan.
- `$spec-implement`: Convenience entry point for implementing the current spec. For substantial work, delegate to the simplified $orchestrator loop; for one already-bounded change, use normal plan -> review -> implementation.
- `$verify-finding`: Verify one disputed, ambiguous or weakly evidenced spec-review misalignment against the spec and repository. Return VERIFIED, REJECTED or BLOCKED.
- `$current-state-capsule`: Produce a short resumable snapshot of the current position in the simplified spec-convergence loop.
- `$terminal-condition`: Optional explicit completion check. In the simplified orchestrator this is equivalent to a fresh exhaustive spec review that returns no material misalignments.
- `$workflow-ontology`: Optional classification helper for naming what kind of repository work a plan or change represents. It does not control the orchestrator loop.
- `$workflow-structure`: Define the minimal AI_SPACE file layout for the simplified spec-review -> workstreams -> plans -> implementation-review loop.

## Supporting planning, review, implementation and learning skills

- `$learn`: Use when the prompt contains [LEARN], or when work has produced lessons, mistakes, debugging discoveries, orchestration lessons, failed plans, validation discoveries or course corrections that should update AI_SPACE/AI_LEARNINGS_LOG.md and AI_SPACE/TODO.md.
- `$retro`: Use when the prompt contains [RETRO], asks for a retrospective, asks whether the agents worked well across sessions, or asks to review process quality, progress rate, efficiency, validation cost, orchestration, handovers, parallelisation, worker behaviour, or AI_SPACE session history. This skill reviews how work was done, not whether the product/research result was good.
- `$maintain-declutter`: Report-only repo declutter and commit-worthiness audit. Use when Codex is asked to review repo files for clutter, permanence, archive recommendations, move recommendations, commit candidates, untracked files, "should this be committed?", "what should be archived?", or file cleanup decisions without changing files.
- `$maintain-despaghettify`: Review repo/codebase structure for spaghettification, tangled responsibilities, code explosions, unclear module boundaries, excessive indirection, duplicated logic, dependency spread, and coupling that distracts from core spec/capability work. Use when Codex is asked to despaghettify, untangle, simplify, or review spaghetti-like code/repo structure, including misspelt prompts such as spagetti.
- `$maintain-elegance`: Review repo-wide codebase elegance across features, APIs, execution paths, logic flow, module boundaries, data flow, abstractions, and capability fit. Use when Codex needs to assess whether the existing repo or merged implementation is as simple, coherent, direct, and spec-focused as reasonably possible.
- `$maintain-review`: Review repo/codebase changes, plans, implementations, or merge candidates for drift away from the project spec and core capabilities. Use when Codex needs to check whether work adds avoidable surrounding software, abstractions, runners, framework code, documentation-only progress, or other repo complexity instead of advancing the project goal.
- `$maintain-techdebt`: Review repo/codebase changes for technical debt, future maintenance cost, brittle implementation, unnecessary dependencies, hard-to-change abstractions, duplicated logic, and debt that blocks or slows core spec/capability progress. Use during plan review, spec review, implementation review, cleanup, and learning when repo maintainability is at stake.
- `$maintain-terminology`: Review input resource (plan, repo, file, document, prompt, ...) for accepted terminology and report on prohibited words and ideas.
- `$first-principles`: This skill should be used when the user asks to "analyze from first principles", "think from scratch", "question this design", "is this the right approach", "why are we doing it this way", "is there a better solution", "challenge assumptions", "should this even exist", or needs to evaluate architectural decisions, design choices, or problem-solving approaches without relying on analogies or conventions.
- `$peer-review`: Review a submitted repo/codebase as a sceptical peer reviewer after reading the associated paper or project claim. Use when Codex needs to assess repo defensibility, reproducibility, implementation correctness, paper-code consistency, function-name versus function-logic mismatches, silent fallbacks, leakage risk, validation reliability, artefact traceability, baseline fairness, or whether the codebase would raise reviewer objections.
- `$plan-elegance`: Review proposed repo changes for solution elegance before implementation. Use when Codex needs to decide whether a plan is the simplest coherent route to the requested capability, fits the existing repo cleanly, avoids unnecessary files/classes/configs/runners/abstractions, and preserves elegant codebase structure.
- `$plan-sub`: Break an accepted plan step into local execution substeps without changing the accepted workstream outcome, scope, requirements or validation intent.
- `$planning-and-task-breakdown`: Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible.
- `$api-and-interface-design`: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.
- `$ask-first`: Ask clarifying questions before executing tasks. Use this skill whenever the user says "ask me questions first", "clarify before doing", "ask before you start", invokes $ask-first, or wants Codex to gather requirements through Q&A before taking action. Also trigger when the user provides a task prefixed with "ask:" or says things like "I need help figuring out how to..." or "help me think through...". This skill ensures nothing is assumed -- Codex asks until 95% confident, then executes.
- `$comprehensive-testing`: Complete testing strategy covering TDD workflow, test pyramid, unit/integration/E2E/property testing, framework best practices (Jest, Vitest, pytest), mock strategies, and CI integration. Use when writing tests, reviewing test quality, or establishing testing standards.
- `$diagnose`: Use when the prompt contains [DIAGNOSE], or when the user asks for the underlying cause of a symptom, failed run, failed test, regression, repeated repair failure, unexpected GPU/CPU/device behaviour, or spec misalignment.
- `$done`: Indicates when the requested work has been completed and validated.
- `$doubt-driven-development`: Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production, security-sensitive logic, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later.
- `$final-report`: Use before [DONE] or [BLOCKED] reports, especially for orchestrated spec implementation.
- `$flowguard`: Guard long, ambiguous, or stateful AI-agent work from drift. Use when the user asks to run or continue a multi-step task, autonomous loop, bug fix, repo change, PR readiness check, compaction handoff, resume from previous context, cost-control checkpoint, or any task likely to span many tool calls, files, sessions, agents, or verification gates.
- `$incremental-implementation`: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.
- `$interface-details`: Bring crafted micro-interactions, thoughtful details, and polish to interfaces. Use when building UI, reviewing UI for detail/polish opportunities, making an interface "feel better," or adding tasteful delight and micro-interactions.
- `$monitor`: Use when the prompt contains [MONITOR], or when a running script, worker agent, validation job or GPU-heavy run needs progress/log/result monitoring, evaluation and possible intervention.
- `$prototype`: Use when the prompt contains [PROTOTYPE], or when one bounded disposable experiment is required to settle an explicit design, behaviour, performance or feasibility decision before durable planning.
- `$simplified-technical-english`: Use when English text must be parsed without a human to resolve ambiguity — tool descriptions, error messages, inter-agent instructions, system prompts, status reports — and misreading has a real cost, or when text reads as dense, hedged, or easy to misparse. Triggers: disambiguate, STE100 rewrite, apply Simplified Technical English, plain-language rewrite, controlled-language rewrite, rewrite so an agent cannot misread this.
- `$test-driven-development`: Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behaviour. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality.

## Discovery

If skill invocation is unavailable, locate the matching `SKILL.md` recursively under `.agents/skills/` using its frontmatter `name`.
