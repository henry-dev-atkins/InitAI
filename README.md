# InitAI

My base AI starting point for my projects.

Copy and paste `AGENTS.md`, `AI_SPACE/`, `.codex/` and `.agents/` into whatever repo you are in. 

Write a file called `SPEC.md`. 
I use ChatGPT maxed out (biggest model, most reasoning, QnA/brainstorm style) to write it, but there is also a skill `spec-write` that you can use. 
My spec files are normally between 10 and 20k lines long.
Put the spec in `AI_SPACE/SPEC.md`.

Then, write a prompt like:

```
\goal Your [TERMINAL_CONDITION] is: "a 6 agent [SPEC_REVIEW] result which finds no difference between the spec and the repo". Please [ORCHESTRATE] until the [TERMINAL_CONDITION] is met. 
```

Then, come back in 10-20 days and you will have your spec.

All work is one branch/checkout at a time, and all agents share the view. Overwriting/conflicts are handled at the planning stage. This is done because it 
1. reduces overhead, and 
2. incentivises the main threead to break work up into independant chunks that are each well defined, and 
3. acts as a good proxy for context degredation. Because the changes/plans are marked as `[BLOCKED]` in an overwrite, when this happens it is not a problem and causes the orchestrator agent to start fresh. A built in context reset.


- Some useful prompts are shared but these are not exhaustive, theyre just examples. 