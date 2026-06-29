---
name: workflow-structure
description: Use when the prompt contains [WORKFLOW_STRUCTURE], or when enforcing the AI_SPACE session, plan, subplan, handover, learning, and TODO structure.
---

# [WORKFLOW_STRUCTURE]
Work in sessions. Each session contains plans. Sessions are joined together by handovers.
Plans, handovers and subplans all follow the naming convention: `TYPE__YYYYMMDD_HHMMSS` where TYPE is either `plan` or `handover`. 
Handovers have the timestamp allocated to the timestamp of their starting plan. The timestamp is the time the plan/handover was created. Subplans are nested within plans, and can be nested to any depth. Each plan/handover has a `plan.md` file that contains the plan/handover details. Plans within plan folders (subplans) represent the Plan B of a Plan A work.
All plans, subplans and handovers adhere to the worktype-ontology. The work type ontology is defined in `.agents/skills/worktype-ontology/SKILL.md`.

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
