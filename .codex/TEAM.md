# Codex Team Model

Use `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` to select the project-scoped `orchestrator` custom agent. The agent loads `$orchestrator` before campaign work.

`.codex/agents/orchestrator.toml` defines the manager identity. `.agents/workflow/workflow.toml` defines mechanical workflow policy, and `.agents/workflow/run.py` enforces its gates and persists session state. `$orchestrator` explains dispatch; the other skills guide judgement. See `.agents/workflow/README.md` for commands and typed handoffs.

## Roles

- `orchestrator`: owns misalignments, workstreams, selection, assignments, verdicts and completion. It never implements project source code.
- `conformance-reviewer`: read-only spec alignment or independent plan review, routed by the task operation.
- `research-architect`: read-only planning for one selected workstream.
- `ml-researcher`: ML/research implementation for one accepted plan.
- `product-engineer`: product/user-flow implementation for one accepted plan.
- `repo-engineer`: repository/config/dependency implementation for one accepted plan.
- `agent-workflow-engineer`: AGENTS/skills/Codex workflow implementation for one accepted plan.
- `validation-engineer`: bounded behavioural validation. It writes only when the accepted plan includes validation files.
- `progress-reporter`: read session evidence and write one progress report in the selected session report directory.
- `merge-captain`: read-only implementation acceptance reviewer.
- `diagnosis-agent`: read-only root-cause investigation.
- `bulk-reader`: optional read-only bounded large-read evidence route.
- `pattern-writer`: optional one-file mechanical implementation after plan acceptance.

## Core execution pattern

Use the operation bindings and transitions in `.agents/workflow/workflow.toml` instead of maintaining another workflow definition here. The orchestrator asks `next` for permitted work, obtains an actual ID from an idle or newly allocated standby instance, reserves the task with `claim`, dispatches work to that instance after success, and submits its result with `complete`. A standby instance must not begin repository work before a successful claim.

Every source-writing task needs acceptance of its current plan and independent implementation review. Rejection returns to planning. Implementation failure is always planning failure. A fresh full conformance `PASS` is the only completion gate.

The runner checks supplied identities, scopes and evidence. It does not authenticate agent instances or launch models. The orchestrator supplies real instance identities, checks that evidence represents actual work, and uses platform sandbox permissions for write enforcement.

Read-only planners and reviewers return exact plan/report/review content and result fields. The orchestrator saves those control files and submits the original worker's claim and instance identity, preserving its facts and verdict. Write-capable workers save only files permitted by their accepted scope and existing permissions. No role gains new source-writing authority through this handoff.

## Concurrency and checkout

- Use the workflow's `max_agents` limit, initially six, when that many useful independent tasks exist.
- The runner counts active DSL claims. The orchestrator must count optional supporting sub-agents against real platform/agent capacity; they are not separate DSL operations.
- The default session uses the current top-level checkout.
- Parallel write agents need accepted plans with non-conflicting read/write scopes and declared resources.
- The runner serialises declared conflicts. Agents must identify semantic conflicts and declare shared git/GPU resources consistently.
- Accepted plans may authorise safe local git work.
- Safe local git includes local branches, worktrees, stage, commit, merge and rebase.
- Serialise git work when it can change shared checkout state.
- Do not push, clean, hard reset, restore or discard paths unless the human explicitly authorises that exact action.

## Skills

The DSL controls mechanical workflow order. Skills remain available as bounded tools for each operation. Supporting skills cannot create new workflow stages, change accepted scope, or choose future work. Preflight follows the workflow file's optional/required policy; command manifests and evidence ledgers are used only when the accepted plan requires them.
