---
name: workflow-structure
description: Enforce AI managed repo structure (plans, handovers, subplans, learnings, todo's) is followed.
--- 

# Workflow
Work in sessions. Each session contains plans. Sessions are joined together by handovers.
Plans, handovers and subplans all follow the naming convention: `TYPE__YYYYHHDD_HHMMSS` where TYPE is either `plan` or `handover`. 
Handovers have the timestamp allocated to the timestamp of their starting plan. The timestamp is the time the plan/handover was created. Subplans are nested within plans, and can be nested to any depth. Each plan/handover has a `plan.md` file that contains the plan/handover details. Plans within plan folders (subplans) represent the Plan B of a Plan A work.

The `AI_SPACE/` folder has structure:
```
AI_SPACE/
  - handovers/
    - handover
  - sessions/
    - session__YYYYMMDD_HHMMSS/
      - plan__YYYYMMDD_HHMMSS/
        - plan.md
        - subplan__YYYYMMDD_HHMMSS/
          - plan.md
          - subplan__YYYYMMDD_HHMMSS/
            - plan.md
          - subplan__YYYYMMDD_HHMMSS/
            - plan.md
    - session__YYYYMMDD_HHMMSS/
      - plan__YYYYMMDD_HHMMSS/
        - plan.md
  ...
```