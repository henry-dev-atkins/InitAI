---
name: workflow-structure
description: Use when the prompt contains [WORKFLOW_STRUCTURE], or when enforcing AI_SPACE session, finding, workstream, plan, review, task packet, result, lock and handover structure.
---

# [WORKFLOW_STRUCTURE]

The orchestrator owns one session with durable finding and workstream registers. Workstreams contain plans, task packets, results and reviews. Sessions are joined by handovers.

All workstreams and plans apply `[WORK_TYPE]` through `$workflow-ontology`.

## Naming

```text
YYYYMMDD_HHMMSS
session__YYYYMMDD_HHMMSS
workstream__WS001__short-name
handover__YYYYMMDD_HHMMSS.md
```

## Structure

```text
AI_SPACE/
  SPEC.md
  TODO.md
  AI_LEARNINGS_LOG.md
  sessions/
    session__YYYYMMDD_HHMMSS/
      session_board.md
      finding_register.md
      workstream_register.md
      locks.md
      workstream__WS001__short-name/
        plan.md
        plan_review.md
        task_packet.md
        result_packet.md
        implementation_review.md
  handovers/
    handover__YYYYMMDD_HHMMSS.md
  archive/
```

## Ownership

The orchestrator owns:

- session board;
- finding/workstream registers and state transitions;
- locks;
- plan/task packet recording;
- agent assignment and integration order;
- final report and commit.

Review/planning agents return bounded reports. Implementation agents own only assigned source edits and their result packet. Workers do not commit.

## Locks

`locks.md` records write scope, stable read assumptions, changed contracts and consumed contracts before implementation starts. Read-only agents may inspect any file. Write agents may edit only assigned scope.
