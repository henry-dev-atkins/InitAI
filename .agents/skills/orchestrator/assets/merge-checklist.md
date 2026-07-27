# Implementation / Integration Review Checklist

For each completed workstream and the accumulated checkout:

- Actual changed files match the accepted task-packet write scope.
- The implementation resolves every assigned source finding.
- Behaviour matches the cited spec requirements.
- Validation commands/results prove the required behaviour.
- No unrelated or extra logic/files were introduced.
- No temporary diagnostics, fluff, legacy compatibility or unapproved workaround remains.
- Parallel writers did not overlap files or violate changed/consumed contract assumptions.
- Accumulated accepted work remains mutually compatible.
- The main thread did not implement project code.

Return `ACCEPT_IMPLEMENTATION`, `REJECT_IMPLEMENTATION` with findings, or genuine `BLOCKED`. Do not prescribe repairs.
