---
name: code-tour
description: Create CodeTour .tour files that guide a specific reader through real code locations. Use for reusable onboarding tours, architecture walkthroughs, pull request reviews, feature explanations, and root cause investigations when a guided code artifact is requested.
---

# Code Tour

Create a coherent walkthrough in `.tours/<reader>-<focus>.tour`. Anchor explanations to the actual repository so the reader can follow the code directly in a CodeTour-compatible editor. Scope the work to tour files unless the user also requests implementation changes.

## Discover the route

Read the relevant repository instructions, README, entry points, configuration, and existing tours. For a pull request tour, inspect the diff and its surrounding code. For a feature or failure tour, trace the execution path and the tests that establish its behavior.

Choose the audience and depth from the request:

| Reader | Emphasis | Typical length |
| --- | --- | --- |
| New contributor | Orientation, key concepts, and the main execution path | 9–13 steps |
| Reader wanting a quick overview | The smallest useful path through the system | 5–8 steps |
| Architect | Boundaries, dependencies, state, and design trade-offs | 14–18 steps |
| Pull request reviewer | Changed behavior, affected boundaries, and supporting tests | 7–11 steps |
| Root cause investigator | Trigger, failure path, cause, and relevant evidence | 7–11 steps |
| Security reviewer | Trust boundaries, validation, authorization, and failure handling | 7–11 steps |
| Feature reader or bug fixer | Inputs, control flow, outputs, and edge cases | 7–11 steps |

Treat these ranges as starting points. Let the requested depth and actual code determine the final length. In a monorepo, stay within the relevant packages and their necessary dependencies.

## Verify the anchors

Read every referenced location before writing its step. Confirm that paths exist, line numbers are in range, selections identify the intended block, and patterns match the intended code.

Use paths relative to the workspace root. Choose one location strategy per step:

| Step type | Fields | Use |
| --- | --- | --- |
| Directory | `directory` | Orient the reader within a module. |
| File and line | `file`, `line` | Point to a specific implementation location. |
| Selection | `file`, `selection.start`, `selection.end` | Highlight a meaningful block. |
| Pattern | `file`, `pattern` | Find a stable declaration when line positions may change. |
| External resource | `uri` | Add a relevant issue, pull request, or document. |
| Content | `description`, optional `title` | Provide a short transition or closing action. |

Include a nonempty `description` for every step. Give steps useful titles. Start with a real file or directory; use content-only steps sparingly.

For selections, use one-based line and character positions. A `pattern` is a regular expression and is considered only when `line` is absent. Escape regex characters and JSON backslashes correctly. 

Never invent an anchor. If repository access is missing, request the relevant files instead of presenting a speculative tour as verified.

## Choose the revision

The optional top-level `ref` associates the tour with a Git branch, commit, or tag. A mismatched revision can make a file unavailable even when it exists in the working directory.

- For a pull request tour, use the pull request branch or a verified commit containing the changes.
- For an onboarding or architecture tour, use the reader's intended revision or omit `ref`.
- For uncommitted files or an uncertain revision, omit `ref` and use the working tree.

When setting `ref`, verify both file existence and anchor correctness at that revision. Do not point a tour of newly added files at the pull request's base branch.

## Write the narrative

Follow a useful route: orientation, module relationships, core execution, a consequential edge case, and the reader's next action. Explain why each step follows the previous one.

Use SMIG to make each substantive description useful:

- **Situation:** Identify what the reader is looking at.
- **Mechanism:** Explain how this code works.
- **Implication:** Explain why it matters to this reader.
- **Gotcha:** Identify a relevant detail the reader could miss.

Use compact prose; explicit SMIG labels are optional. Do not invent a gotcha merely to fill the pattern. Separate observed behavior from an inference about design intent.

For pull requests, prioritize changed behavior and include unchanged code when necessary to explain its effect. For investigations, distinguish a demonstrated cause from a hypothesis. Finish with an action the reader can now perform.

## File format

Write valid JSON with a title and an ordered, nonempty `steps` array. The following illustrates the structure; replace its example paths and line number with verified locations:

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Request validation tour",
  "description": "Follow a request from entry to validation.",
  "steps": [
    {
      "directory": "src",
      "title": "Locate the request path",
      "description": "Start in the runtime source tree, then follow the request entry point."
    },
    {
      "file": "src/server.ts",
      "line": 12,
      "title": "Enter the handler",
      "description": "This handler receives the request and passes its input to validation before dispatch. Follow the validator to see which inputs can reach the service."
    }
  ]
}
```

## Validate and deliver

Parse the JSON and check the current schema when available. Verify every location in the intended revision and check that descriptions match the code. Read the tour in order to catch unexplained jumps, repeated steps, and generic descriptions.

Report the created file, intended reader, scope, and validation performed. Distinguish JSON and anchor checks from actual playback in an editor; claim playback only if performed.
