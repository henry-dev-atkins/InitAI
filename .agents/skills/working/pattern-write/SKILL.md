---
name: pattern-write
description: Apply one mechanical, one-file implementation change from one existing reference after an accepted plan.
---

# Pattern write

Use only when the orchestrator has an accepted plan and the change is mechanical.

State the exact target file, parent reference, contract, differences, preserved invariants, and validation command before editing.

Create or replace exactly one new file from one reference. Keep the change local and current-state only.

Do not change dependencies, schemas, public APIs, security rules, concurrency, migrations, shared state, adjacent files, or workflow contracts. Do not spawn agents or run git commands.

Report through the existing `implementation` result contract. Do not invent a `PATTERN_WRITE` operation or result schema.
