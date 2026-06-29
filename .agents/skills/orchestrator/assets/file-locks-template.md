# File Ownership Locks

| File/Path | Owner Plan | Owner Agent | Mode | Status |
|---|---|---|---|---|
| `AI_SPACE/SPEC.md` | none | none | locked | spec-edit-only |
| `{path}` | PXXX | `{agent-name}` | write | active |

Rules:

- Read-only agents may inspect any file.
- Write agents may edit only paths explicitly assigned to them.
- Two write agents may not own the same file/path unless work is serialised by the orchestrator.
- Lock changes must be recorded before agents act on them.
