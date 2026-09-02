---
name: code-style
description: Use when Codex should write, review, refactor, or plan code.
---

# Code Like Henry
Write code where the main idea is easy to see.

# Main Logic holds Center Stage
If I cannot run it in my head, it is too hidden.
Prefer code that feels like a proof you can run.
Keep the mechanism in view, no obscuring logic.
The best version is not the most layered version, but the one where the working reason is visible.
They should not need to reconstruct it from helpers, registries, factories, and lifecycle objects.
Use direct code for the important path.
Do not make me reverse-engineer the intention.
Code should have a centre of gravity.
The design should survive being read backwards.


# Infra Bloat
Keep contracts small: An interface is a promise, Promise less to Keep more freedom.
A good interface says only what its caller needs, For example:
```python
class Estimator:
    def observe(...)
    def estimate(...)
```
A bad interface predicts a whole future system.
It makes simple work ask permission from architecture.
"Evidence watches the run." - Logs, metrics, and artefacts should observe behaviour.
They should not become the behaviour.
Abstraction is debt until it pays rent.
Infrastructure is background.


## Names
Use names that come from the problem (maths, domain, task, ...).
Short names are fine when they are true but long names are bad when they replace understanding.
Prefer concrete names:
```python
active = select_active(...)
estimate = estimator.estimate(active, observed)
apply_update(estimate)
```
Avoid inflated names:
```python
resolved_capability_execution_payload = ...
```
Do not hide the path behind generic lifecycle language.
Infra shoudl NEVER become the code, it is a watcher. 
No serious-sounding fog.
A name should reduce thinking.

## Avoid
Avoid framework code that becomes the product.
Avoid broad registries unless they replace real repeated code.
Avoid one use wrappers unless they protect a real invariant.
Avoid names that sound precise but hide the simple action.
Avoid splitting the algorithm until the split makes the algorithm easier to read.

## Review Question
Before finishing, ask:
- Can a new reader explain the core loop without opening five files?
- Where is the core loop?
- Can I read it without chasing abstractions?
- Does each helper remove clutter from that loop?
- Did any safety rule obscure the reason this works?
- Would the first proof-of-concept still recognise itself here?


## Explicit Code Style:
1. Prefer if, elif, else over basic if/else chains.
2. Indentation should follow on from brackets, Examples:
```python
function_call(
    arg1,
    arg2,
    arg3
)
->
function_call(
            arg1,
            arg2,
            arg3
            )
```
or
```python
if step != self._last_completed_step + 1:
    raise CATLifecycleError(
        f"CAT steps must be strictly monotonic; expected {self._last_completed_step + 1}, got {step}."
    )
->
if step != self._last_completed_step + 1:
    raise CATLifecycleError(
                            f"CAT steps must be strictly monotonic; expected {
                            self._last_completed_step + 1}, got {step}."
                            )
```
or
```python
self._active_schedule_hasher.update(
        json.dumps(
            schedule_payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
->
self._active_schedule_hasher.update(
                                    json.dumps(
                                                schedule_payload,
                                                sort_keys=True,
                                                separators=(",", ":"),
                                                ).encode("utf-8")
                                    )
```
or
```python
def estimate_dormant(
    self,
    selection: ActiveSelection,
    g_A: Any,
    *,
    step: int,
) -> EstimateResult:
    """Query dormant values from the last committed estimator state."""
->
def estimate_dormant(
                    self,
                    selection: ActiveSelection,
                    g_A: Any,
                    *,
                    step: int,
                    ) -> EstimateResult:
    """Query dormant values from the last committed estimator state."""
# or even better:
    def estimate_dormant(self,selection: ActiveSelection,g_A: Any,*,step: int,) -> EstimateResult:
        """Query dormant values from the last committed estimator state."""
```
or
```python
def diagnostic_summary(self) -> dict[str, Any]:
    """Return constant-size factual CAT lifecycle diagnostics."""

    return {
        "temporal_fill_truth_firewall_passed": True,
        "dense_guard": (
            self.dense_guard.summary()
            if self.dense_guard is not None
            else {
                "format_version": "cat_dense_guard_v1",
                "passed": True,
                "applicability": "diagnostic_or_non_systems_route",
                "evidence_source": "not_instrumented",
            }
        ),
    }
->
def diagnostic_summary(self) -> dict[str, Any]:
    """Return constant-size factual CAT lifecycle diagnostics."""

    return {
            "temporal_fill_truth_firewall_passed": True,
            "dense_guard": (
                            self.dense_guard.summary()
                            if self.dense_guard is not None
                            else {
                                "format_version": "cat_dense_guard_v1",
                                "passed": True,
                                "applicability": "diagnostic_or_non_systems_route",
                                "evidence_source": "not_instrumented",
                                }
                            ),
            }
```

3. All functions/classes should have docstrings, with parameters [inputs/outputs, (shapes, types), assumptions, operations, use case].
4. Type hint everywhere.
5. Function structure should generally be: 1) docstring, 2) type hints, 3) input validation, 4) main logic, 5) return statement.
6. Comments should be used to explain why and how something is done, not what is done. The code itself should be clear enough to convey the "what."
7. Blank lines depend on seperation of code types. Between classes: 3, between functions: 2, between code blocks: 1.