# Hook and Interface Contract

**Version:** 1.1.0
**Last updated:** 2026-04-06
**Status:** Authoritative — this document reflects the current implementation

---

## Overview

The hook system allows external code and internal runtime components to intercept and influence execution at defined points. There are two distinct hook layers:

1. **Claude Code hooks** (`hooks/hooks.json`) — prompt and command hooks that Claude Code fires at conversation-level events (`UserPromptSubmit`, `PreToolUse`). These are Claude Code platform hooks, not Python pipeline hooks.
2. **Python runtime hooks** (`hooks/*.py` + `HookRegistry`) — Python functions registered with `HookRegistry` that the `RuntimeDispatcher` and `TransitionEngine` fire at pipeline execution events.

This document covers both. They are complementary, not interchangeable.

---

## Claude Code Hooks (`hooks/hooks.json`)

### Configured hooks

| Event | Hook type | Purpose |
|---|---|---|
| `UserPromptSubmit` | Prompt | Trace microcheck supervisor — evaluates active pipeline state before responding |
| `PreToolUse` (Bash) | Prompt | Trust verification — blocks Forge/Inquiry execution if no Forensics trust_zone_map exists |
| `PreToolUse` (shell) | Command | Destructive command blocking via `hooks/block_destructive_commands.py` |

### Trace microcheck (UserPromptSubmit)

Before every response, when a pipeline is active, the Trace supervisor silently evaluates:

1. Is the current approach still in the right phase for the active pipeline?
2. Has a pivot condition fired?
3. Is confidence outrunning evidence quality?
4. Are there too many live branches without discrimination?
5. Has trust collapsed enough to require a Forensics reset?
6. Can the next move be handled with a smaller intervention than currently planned?

Findings surface at the top of the response only when a real condition is present. No fabricated checks.

### Trust verification (PreToolUse/Bash)

Before any Forge or Inquiry pipeline invocation via Bash, checks for `runtime_output/Forensics/project_mapping/trust_zone_map.yaml`. If absent, returns `ask_user` with a message that Forensics ground truth must be established first.

Forensics, Conduit, and unrelated commands: approved without comment.

---

## Python Runtime Hooks

### Hook events

| Event | When | Fires in |
|---|---|---|
| `PRE_PIPELINE` | Before pipeline execution begins | `RuntimeDispatcher.execute_pipeline()` |
| `POST_PIPELINE` | After pipeline execution completes | `RuntimeDispatcher.execute_pipeline()` |
| `PRE_TRANSITION` | Before any high-impact state transition | `TransitionEngine._fire_pre_transition()` |
| `PRE_PHASE` | Before a phase executes | _Defined, not yet wired_ |
| `POST_PHASE` | After a phase executes | _Defined, not yet wired_ |
| `PRE_ROUTE` | Before a route decision | _Defined, not yet wired_ |
| `POST_ROUTE` | After a route decision | _Defined, not yet wired_ |
| `ON_ERROR` | When execution error occurs | _Defined, not yet wired_ |
| `ON_CHECKPOINT` | When checkpoint is created | _Defined, not yet wired_ |

### Currently registered hooks

| Hook | Event | Priority | File |
|---|---|---|---|
| `validate_entry_hook` | `PRE_PIPELINE` | 10 | `hooks/pre_pipeline.py` |
| `review_output_hook` | `POST_PIPELINE` | 10 | `hooks/post_pipeline.py` |
| `trigger_ownership_hook` | `PRE_TRANSITION` | 15 | `hooks/trigger_ownership.py` |

### Hook interface

```python
def my_hook(context: HookContext) -> HookResult:
    ...
```

```python
@dataclass
class HookContext:
    session_id: str           # e.g. "Forge/development"
    pipeline_id: str          # e.g. "Forge/development"
    phase_id: str | None      # current phase name, or None
    state: ExecutionState     # live execution state (read-only by convention)
    context: Dict[str, Any]   # pipeline context + any hook-injected data
    timestamp: str            # ISO format
```

```python
@dataclass
class HookResult:
    continue_execution: bool = True
    modifications: Dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None

    @classmethod
    def success(cls, modifications=None) -> HookResult: ...

    @classmethod
    def halt(cls, error_message: str) -> HookResult: ...
```

A hook returning `HookResult(continue_execution=False)` halts execution. The first halt wins — subsequent hooks for that event do not run.

### Hook registration

```python
registry = HookRegistry()
registry.register(HookEvent.PRE_PIPELINE, my_hook, priority=10)
# Higher priority runs first. Default: 0.
```

Registration happens in `RuntimeDispatcher._build_hook_registry()`.

---

## PRE_PIPELINE: `validate_entry_hook`

### Behaviour

1. Validates pipeline ID format (`Family/pipeline_name`)
2. Validates family is one of: `Forensics`, `Forge`, `Inquiry`, `Conduit`
3. Checks execution state has no pre-existing errors
4. Loads the pipeline's YAML spec from `entrypoints/<Family>/pipelines/<pipeline_name>/pipeline.yaml`
5. Evaluates `entry_conditions` from the YAML spec against the provided context

### Entry condition evaluation

Entry conditions are semantic string identifiers (e.g., `project_state_is_grounded_enough_for_build_work`). Evaluation uses a two-tier approach:

**Mapped conditions** — conditions with a known context key requirement:

| Condition | Required context key |
|---|---|
| `project_state_is_grounded_enough_for_build_work` | `problem` |
| `a_buildable_problem_is_defined` | `problem` |
| `a_coding_change_is_scoped` | `change_type` |
| `test_scope_is_defined_or_implied_by_state` | `test_scope` |
| `handoff_state_exists_in_artifacts` | state artifacts (must be non-empty) |
| _(see `hooks/pre_pipeline.py` for full mapping)_ | |

**Blocking negation conditions** — if these appear in entry_conditions and the corresponding violation key is set in context, halt:

| Condition | Violation key |
|---|---|
| `ground_truth_is_sufficiently_stable_or_forensics_has_bounded_the_surface` | `ground_truth_unstable` |
| `no_active_trust_collapse` | `trust_collapsed` |

**Unmapped conditions** — semantic preconditions with no programmatic check. These pass silently. They are intent-level gates enforced by the caller's context-setting, not by the hook.

### Return

On failure: `HookResult.halt(f"Pipeline '{pipeline_id}' entry conditions not satisfied: ...")`
On spec not found: `HookResult.success(modifications={"entry_condition_warning": ...})`
On success: `HookResult.success(modifications={"entry_conditions_checked": [...], "entry_conditions_satisfied": True})`

---

## PRE_TRANSITION: `trigger_ownership_hook`

### Purpose

Enforces the trigger ownership model from `docs/implementation/trigger_patterns.md` before any high-impact transition executes.

### Fires for

`TransitionEngine` fires `PRE_TRANSITION` before: `AUTHORITY_CALL`, `CROSS_FAMILY_REROUTE`, `SIBLING_SHIFT`, `FORENSICS_RESET`.

Does **not** fire for `CONTINUE` or `PHASE_PIVOT`.

### Context keys (populated by TransitionEngine)

```python
{
    "pending_action":         str,   # RouteAction.value
    "pending_target":         str,   # e.g. "authority:Lever"
    "pending_trigger":        str,   # trigger ID
    "pending_authority_data": dict,  # authority_data from RouteDecision
}
```

### Rules enforced

**Rule 1 — Lever after Trace**

Lever (`authority:Lever`) may not be called unless:
- `_authority_trace_evaluation` is present in state artifacts, **or**
- `trace_consulted: true` is set in context

Violation: `"Trigger ownership violation: Lever evaluator '...' called before Trace attempted smallest-sufficient handling."`

Fix: Dispatch to `authority:Trace` first, or set `trace_consulted: true` in context if Trace was consulted via an inline path.

**Rule 2 — No Residue-as-adjudicator**

Residue (`authority:Residue`) may not be called with a non-Residue-domain signal when adjudication-requiring artifacts are present in state (`contradictions_detected`, `support_gap`, `frame_error_risk`, `discriminator_required`).

Violation: `"Trigger ownership violation: Residue called with signal '...' while adjudication-requiring artifacts are present."`

Fix: Use `authority:Lever` with the appropriate evaluator for explicit adjudication.

**Rule 3 — No premature cross-family reroute**

`CROSS_FAMILY_REROUTE` may not be triggered while `local_pivot_available: true` is set in context and no trust collapse indicators are present.

Violation: `"Trigger ownership violation: cross-family reroute triggered while a legal local intervention ('local_pivot_available' is set) remains."`

Fix: Apply the smallest-sufficient local intervention first (phase pivot, sibling shift).

**Rule 4 — Residue-domain signals through Residue first**

Residue-domain signals (`misfit_detected`, `absence_detected`, `tension_detected`, `warp_detected`, `offset_detected`) must dispatch to `authority:Residue` before `authority:Lever`. Lever may not be called for these signals unless:
- `_authority_residue_recommendation` is present in state artifacts, **or**
- `residue_consulted: true` is set in context

Violation: `"Trigger ownership violation: Lever called for Residue-domain signal '...' without first consulting Residue."`

Fix: Dispatch to `authority:Residue` first.

---

## POST_PIPELINE: `review_output_hook`

Reviews pipeline output after execution. Checks for:
- Required artifacts present
- Route recommendation populated
- No unresolved errors blocking handoff

Returns `HookResult.success()` with any quality observations in `modifications`.

---

## Authority dispatch (via TransitionEngine)

When `TransitionEngine` processes an `AUTHORITY_CALL` decision (after `PRE_TRANSITION` hooks pass), it dispatches to the appropriate authority handler:

| Target | Handler | Records artifact |
|---|---|---|
| `authority:Trace` | `TraceSelector.evaluate()` + `smallest_intervention()` | `_authority_trace_evaluation` |
| `authority:Lever` | `LeverEscalation.evaluate(evaluator_id, context)` | `_authority_lever_result` |
| `authority:Residue` | `ResidueDispatch.dispatch(signal, context)` | `_authority_residue_recommendation` |

Authority data is passed via `RouteDecision.authority_data`:

```python
RouteDecision(
    action=RouteAction.AUTHORITY_CALL,
    target="authority:Lever",
    authority_data={
        "evaluator_id": "contradiction_evaluator",
        "context": {...},
    },
    ...
)
```

---

## Hook best practices

1. **Fail fast** — Hooks block execution. Keep them under 100ms. Long-running validation belongs in a PostPipeline hook, not PrePipeline.
2. **Idempotent** — Hooks may be retried if the registry executes them in a retry loop. Do not produce side effects that must be undone.
3. **Signal via context, not exceptions** — Return `HookResult.halt(message)` rather than raising. Exceptions are caught and converted to halt results, but the error message is less precise.
4. **Don't mutate state** — `HookContext.state` is passed by reference. Mutations will affect live execution state. Only modify `context.context` via the `modifications` return key.
5. **Use bypass keys for legitimate shortcuts** — If your caller has a valid reason to skip a rule (e.g., Trace was consulted inline), set the bypass key (`trace_consulted: true`) rather than trying to work around the hook.

---

## Testing hooks

```python
from hooks.context import HookContext, HookResult
from hooks.pre_pipeline import validate_entry_hook
from runtime.state.models import ExecutionState, FamilyType

def test_validate_entry_hook_blocks_missing_problem():
    state = ExecutionState(current_family=FamilyType.FORGE)
    ctx = HookContext(
        session_id="test",
        pipeline_id="Forge/development",
        phase_id=None,
        state=state,
        context={},  # no "problem" key
    )
    result = validate_entry_hook(ctx)
    assert not result.continue_execution
    assert "'problem'" in result.error_message
```

```python
from hooks.trigger_ownership import trigger_ownership_hook

def test_lever_without_trace_blocked():
    state = ExecutionState(current_family=FamilyType.FORGE)
    ctx = HookContext(
        session_id="test",
        pipeline_id="Forge/coding",
        phase_id=None,
        state=state,
        context={
            "pending_action": "authority_call",
            "pending_target": "authority:Lever",
            "pending_authority_data": {"evaluator_id": "trust_evaluator"},
        },
    )
    result = trigger_ownership_hook(ctx)
    assert not result.continue_execution
    assert "Trace" in result.error_message
```

---

## Extension points

To add a new Python hook:

1. Create `hooks/my_hook.py` with a function `my_hook(context: HookContext) -> HookResult`
2. Import and register in `RuntimeDispatcher._build_hook_registry()`:
   ```python
   from hooks.my_hook import my_hook
   registry.register(HookEvent.POST_PIPELINE, my_hook, priority=5)
   ```
3. Export from `hooks/__init__.py`
4. Add tests in `tests/runtime/`

To wire a currently-unwired event (e.g., `PRE_PHASE`):
1. Add the firing call in the appropriate runtime method (analogous to `TransitionEngine._fire_pre_transition`)
2. Populate the relevant context keys the hook will read
3. Document the context key contract in this file
