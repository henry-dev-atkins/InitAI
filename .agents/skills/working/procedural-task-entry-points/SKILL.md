---
name: procedural-task-entry-points
description: Prefer one procedural entry point for a concrete application task instead of a shared continuation-registration gate.
---

# Procedural task entry points

Use this skill when callers register pending callbacks into a shared offer,
proceed, consent, confirmation, or resume helper.

## Invariant

The concrete task owns its story. A reader should understand the task by reading
one entry point. The reader should not reconstruct a registration protocol across
several modules.

## Preferred shape

1. Create one entry point for each concrete user task.
2. Keep the entry point procedural. Check the precondition. Seek agreement when needed. Abandon on decline. Run the task after agreement.
3. Keep shared code as a thin subroutine that checks the precondition.
4. Define dialog and prompt callbacks at or beside the entry point.
5. Run the task unconditionally after the precondition succeeds.

## Reject this shape for linear task journeys

- A caller registers a pending action for a shared helper to resume.
- An entry point only creates callback data and calls `offer` or `proceed`.
- One module owns the gate, side effects, and the caller continuation.
- Hidden module state tells a dialog which task to run.
- A renamed action bag keeps the same inverted control.

## Valid exception

A shared wrapper is valid when the wrapper itself is the product story. Use it for
a narrow, repeated mechanical envelope such as obtaining a token, retrying, or
bridging callbacks to async code. Do not use it for heterogeneous user tasks.

Apply this rule in any programming language. The motivating examples include
JavaScript and TypeScript user interfaces.
