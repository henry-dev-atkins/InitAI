---
name: teach
description: Explain a repository feature or change so a non-domain-expert reader understands what it is, how it works, and why it exists. Use for teaching requests, not implementation.
---

# Teach

Explain the smallest complete model first.

Begin with what the feature is and the problem it solves.

Then trace one representative path through the real files.

Explain the reason for each important step.

Use a small diagram only when three or more moving parts are easier to follow visually.

Use `$why` for design rationale when the user needs historical or causal evidence.

Use `$implementation-desk-check` when a control-flow trace is enough.

Use `$first-principles` when the user is questioning the design itself.

Keep observations separate from inferences.

Do not change files while teaching unless the user asks for implementation.

Match depth to the question. Stop after the first useful explanation when the user did not ask for a tutorial.

Write the explanation itself. Do not report the teaching process.
