# File, Contract and Resource Locks

| Workstream | Owner Agent | Write Scope | Stable Read Scope | Contracts Changed | Contracts Consumed | Mutable Resources | Status |
|---|---|---|---|---|---|---|---|
| WSXXX | `{agent-name}` | `{exact paths}` | `{exact paths}` | `{CON IDs}` | `{CON IDs}` | `{resource IDs}` | reserved |

Rules:

- Read-only agents may inspect any file.
- Write agents may edit only paths assigned to their workstream.
- Active workstreams must have disjoint write scopes.
- An active write scope must not overlap another workstream's stable read scope.
- A changed contract must not be consumed or changed by another active workstream.
- Shared generated files, manifests, lockfiles, registries, migrations, ports, databases, GPUs, caches, datasets and environments require explicit single ownership through `Mutable Resources`.
- Lock changes are recorded before agents act.
