---
name: why
description: Investigate why a repository design, change, threshold, or failure exists using local code, tests, history, and recorded evidence. Use for design rationale and postmortem questions.
---

# Why

Explain the forces that shaped a repository decision.

Start with a concrete target. Name the file, symbol, behaviour, or change under review.

Read the current implementation before forming a theory.

Use tests, configuration, plans, learnings, and local history as evidence.

Use `git log`, `git blame`, and `git show` when history can answer the question.

Separate these statements:

- observed in the repository
- supported by history or tests
- inferred from the available evidence
- still unknown

State the strongest explanation that the evidence supports.

Do not invent an issue, pull request, external system, or author intent.

If the evidence is missing, say what is missing and stop the claim there.

For a design choice, describe the constraint, the chosen response, the rejected cost, and the evidence.

For a failure, describe the trigger, mechanism, missed check, and smallest durable correction.

Return a concise explanation with repository paths and line references where they matter.
