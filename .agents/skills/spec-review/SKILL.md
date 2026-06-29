---
name: SPEC_REVIEW
description: Compares implementation to the specification and identifies misalignments.
--- 

# Workflow

Compare implementation to the specification (may be a subset of spec).
  - Check alignment agentically by type:
      - Capability
      - Logic
      - Implementation
      - Correctness
      - Documentation
      - Outputs
      - Defensibility
      - Implementation Laziness
  - Write each misalignment point into the `AI_SPACE/TODO.md`, in order of severity and grouped by issue.



  
- Spec will have a walkthrough section with work stages/steps/milestones.
- Spec doc is generally the guide to build the project, not its usage, for example:
    - The steps to build a research suite, not the actual experiments.
    - The steps to build an app, not the actual app itself.
- The 'usage' comes later, and generally the spec is swapped out for an explicit 'implementation guide'.