[SESSION.START] [TEAM] [agentic] $orchestrator

Act as the main orchestrator for this session.

Goal:
{session-goal}

Inputs:
- Read `AGENTS.md`.
- Read `AI_SPACE/SPEC.md`.
- Read `AI_SPACE/TODO.md`.
- Read recent handovers, session boards, plans and learnings.

Required behaviour:
1. Build a session board.
2. Classify work using `[WORK_TYPE]`.
3. Create one plan packet per independent work package.
4. Review the board and packets before spawning implementation agents.
5. Spawn domain expert agents for independent work.
6. Use separate branches/worktrees for durable write packages.
7. Allow worker agents to spawn read-only subagents for exploration, review and diagnosis.
8. Do not allow nested write agents unless the task packet explicitly permits it.
9. Collect structured result packets.
10. Review, validate and merge serially.
11. Update TODOs/learnings/handovers where relevant.
12. End with `[DONE]` or `[BLOCKED]` according to the repo final report contract.

Default limits:
- Maximum parallel write-capable work packages: 4.
- Maximum read-only/review agents: 6.
- Maximum nested depth: 2 only when the session board explicitly justifies it.

GPU policy:
Only one GPU is assumed. Do not schedule multiple GPU-heavy validation runs concurrently.
