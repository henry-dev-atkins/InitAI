---
name: workflow-structure
description: Use when the prompt contains [WORKFLOW_STRUCTURE], or when enforcing the AI_SPACE session, plan, subplan, handover, learning, TODO, task packet, result packet and lock structure.
---

# [WORKFLOW_STRUCTURE]

Work in sessions. Each session contains plans. Plans may contain subplans. Sessions are joined together by handovers.

All plans, subplans and handovers must follow `[WORK_TYPE]`.

## Naming

Use timestamps in this form:

```text
YYYYMMDD_HHMMSS
```

Use folder names:

```text
session__YYYYMMDD_HHMMSS
plan__P001__short-name
subplan__P001A__short-name
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
      locks.md
      plan__P001__short-name/
        plan.md
        task_packet.md
        result_packet.md
        subplan__P001A__short-name/
          plan.md
          task_packet.md
          result_packet.md
  handovers/
    handover__YYYYMMDD_HHMMSS.md
  archive/
```

## Orchestrated sessions

`$orchestrator` owns:

- `session_board.md`
- `locks.md`
- plan packet creation
- merge order
- session-level final report

Worker/domain agents own:

- assigned plan implementation
- assigned `result_packet.md`
- validation evidence inside approved output locations
- edits only their assigned files in the current checkout; workers do not commit

## File locks

Use `locks.md` to state write ownership before agents start. Read-only agents may inspect any file. Write-capable agents may edit only their assigned scope.
