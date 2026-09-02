---
name: requirements-discovery
description: Optional read-only exploration used when the spec or repository area is not yet clear enough for a confident spec review or plan. Use when the prompt contains [SPEC.EXPLORE] or capabilities are asked for, when a large or uncertain request cannot yet be converted into decision-complete workstreams, or when repeated replanning indicates unresolved specification fog.
---

# [SPEC.EXPLORE]

Map uncertain spec territory until the destination, blocking questions and candidate durable outcomes are explicit enough for portfolio planning. Do not implement, authorise work or disguise unresolved decisions as plans. Explore one bounded uncertainty and return evidence that helps `$conformance` or `$plan` make a decision.

Do not create durable implementation scope, workstreams, or workflow state. If a disposable experiment is genuinely required to settle the uncertainty, classify the question as `EVIDENCE_BLOCKED` and state the smallest experiment or observation needed. Do not run that experiment inside this read-only skill.


## Exploration model

Classify each relevant question as:

- `SETTLED`: authority or evidence already answers it;
- `ANSWERABLE_NOW`: repository inspection or bounded research can answer it;
- `EVIDENCE_BLOCKED`: the question is precise but needs a named observation, benchmark or prototype;
- `FOG`: the question itself cannot yet be stated precisely enough for implementation planning.

A candidate outcome is `COMMITTED` only when its mission, authority, dependencies and proof can be stated. Otherwise retain it as `PREPARED` or fog.
