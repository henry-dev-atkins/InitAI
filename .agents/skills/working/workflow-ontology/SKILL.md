---
name: workflow-ontology
description: Optional classification helper for naming what kind of repository work a plan or change represents. It does not control the orchestrator loop.
---

# [WORK_TYPE]

Classify work when the distinction is useful:

- `CAPABILITY.RESEARCH`
- `CAPABILITY.PRODUCT`
- `FIX.ALIGNMENT`
- `EVIDENCE.VALIDATION`
- `ENVIRONMENT.ADAPTATION`
- `TEMPORARY.DIAGNOSTIC`
- `FLUFF.DISPOSABLE`
- `DOCS.MEMORY`
- `AGENT.WORKFLOW`
- `CLEANUP.HYGIENE`
- `SPEC.EDIT`

Return the primary work type and one-line reason.

This label does not add gates, states, commits, manifests, or scheduling rules.
