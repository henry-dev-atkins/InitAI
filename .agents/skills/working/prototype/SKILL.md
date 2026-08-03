---
name: prototype
description: Use when the prompt contains [PROTOTYPE], or when one bounded disposable experiment is required to settle an explicit design, behaviour, performance or feasibility decision before durable planning.
---

# [PROTOTYPE]

Create disposable primary evidence for one explicit decision. A prototype settles a decision; it does not earn a place in production.

## Hard boundary

- The prototype is temporary work, not product implementation or capability progress.
- It must not enter active imports, execution paths, configuration, packaging or generated product outputs.
- It must not become a compatibility layer, workaround or unreviewed foundation.
- Do not broaden beyond the single stated question.
- Do not commit the prototype as active product code.

## Location

Use a bounded repo-local experiment path:

```text
AI_SPACE/experiments/EXPXXX__short-name/
  question.md
  prototype/
  commands.md
  result.md
```

If the repository policy requires active-session locality, place it beneath the current session and archive it after the decision. Never scatter prototype files through product paths.

## Required inputs

- one precise decision question;
- competing hypotheses or behaviours;
- success/failure observations;
- allowed temporary write scope;
- resource and safety constraints;
- owning exploration/finding/workstream ID.

## Execution rules

- Use the smallest experiment that can discriminate between hypotheses.
- Record exact commands, environment facts and observations.
- Prefer real interfaces and data shapes where safe, but do not harden the prototype into production structure.
- Fail loudly when the experiment cannot answer the question.
- Remove or archive temporary caches and outputs after recording evidence.

## Output

```yaml
prototype_id: EXP001
owner: {SE/FV/WS ID}
question: {one explicit decision}
hypotheses: []
method: []
artefact_path: {AI_SPACE experiment path}
observations: []
decision_evidence: {what the experiment establishes}
limitations: []
status: DECISION_SUPPORTED | DECISION_NOT_SUPPORTED | INCONCLUSIVE | BLOCKED
archive_required: true
```

The calling skill or orchestrator records the durable decision separately. Prototype contents remain historical evidence only.
