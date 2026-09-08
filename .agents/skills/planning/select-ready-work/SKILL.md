---
name: select-ready-work
description: Select the next N useful ready independent workstreams from the current workstream list for planning or implementation.
---

# [PORTFOLIO.NEXT] / select-ready-work

Input: current workstreams and available agent capacity.

Output: selected workstream IDs in priority order.

Prefer the largest useful independent workstreams that are executable now.

Rank by:

1. amount and importance of spec misalignment resolved;
2. unblock value;
3. core behaviour before cleanup;
4. confidence that the workstream can proceed independently;
5. low collision risk with other selected workstreams.

N is a maximum. 
Never invent work or select unsafe work merely to fill capacity.

Do not plan the selected workstreams. Do not change their outcome boundaries.
