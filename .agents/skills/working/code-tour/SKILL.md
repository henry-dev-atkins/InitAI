---
name: code-tour
description: Create a verified CodeTour file that guides a specific reader through real repository locations.
---

# Code tour

Use this skill when the user requests a reusable walkthrough of code, a change, an architecture path, or a root cause.

Read repository instructions, the relevant entry points, configuration, tests, and existing tours before writing. Choose the smallest route that answers the reader's question.

Write the tour to `.tours/<reader>-<focus>.tour` only when a tour is requested. Use relative paths and valid CodeTour JSON with a title, description, and nonempty ordered `steps` array.

Every step must have a useful title, a nonempty description, and one verified location. Use a directory, file and line, selection, pattern, external URI, or short content transition. Prefer patterns when line numbers are likely to change.

Read every referenced location before writing it. Confirm that paths exist, line numbers are in range, selections identify the intended block, and patterns match. Never invent an anchor.

Omit `ref` for uncertain or uncommitted revisions. Include it only after verifying the same anchors at that revision.

Build the route from orientation to execution, a consequential edge case, and the reader's next action. Explain the situation, mechanism, implication, and relevant gotcha when the code supports them.

Validate the JSON, anchors, descriptions, step order, and navigation jumps. Report static validation separately from editor playback. Do not claim playback without opening the tour in a compatible editor.
