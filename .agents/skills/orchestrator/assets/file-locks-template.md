# File and Contract Locks

| Workstream | Owner Agent | Write Scope | Stable Read Scope | Contracts Changed | Contracts Consumed | Status |
|---|---|---|---|---|---|---|
| WSXXX | `{agent-name}` | `{paths}` | `{paths}` | `{interfaces/schemas/configs}` | `{interfaces/schemas/configs}` | reserved |

Rules:

- Read-only agents may inspect any file.
- Write agents may edit only paths assigned to their workstream.
- Active workstreams must have disjoint write scopes.
- A changed contract must not be consumed as stable by another active workstream.
- Shared generated files, manifests, lockfiles, registries and migrations require explicit single ownership.
- Lock changes are recorded before agents act.
