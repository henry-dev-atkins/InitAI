# InitAI

My base AI starting point for my projects.

Copy and paste `AGENTS.md`, `AI_SPACE/`, `.codex/`, `.agents/` and `tools/` into whatever repo you are in. 

Write a file called `SPEC.md`. 
I use ChatGPT maxed out (biggest model, most reasoning, QnA/brainstorm style) to write it. 
My spec files are normally between 10 and 20k lines long.
Put the spec in `AI_SPACE/SPEC.md`.

Then, write a prompt like:

```
\goal Your [TERMINAL_CONDITION] is: "a 6 agent [SPEC_REVIEW] result which finds no difference between the spec and the repo". Please [ORCHESTRATE] until the [TERMINAL_CONDITION] is met. 
```

Then, come back in 10-20 days and you will have your spec.


```text
review spec
-> misalignments
-> collate into independent workstreams
-> select next N
-> plan each workstream
-> review each plan
-> implement accepted plans + independently review them
-> review spec again
```




