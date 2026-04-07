# ADR-002: Trigger Ownership Enforcement via PRE_TRANSITION Hook

**Status:** Accepted
**Date:** 2026-04-06
**Deciders:** Ash (author), Claude (implementation agent)
**Supersedes:** n/a
**Related:** ADR-001 (authority architecture)

---

## Context

ADR-001 established that Trace, Lever, and Residue are distinct authorities with distinct ownership over different classes of supervisory action. The `docs/implementation/trigger_patterns.md` specification defines this formally:

- **Trace** owns routine micro-checks, smallest-sufficient intervention choice, ordinary routing supervision
- **Residue** owns suspicious-surface interpretation, lens-based first responses, anomaly shaping
- **Lever** owns evaluator invocation, explicit adjudication, escalation, commitment and reopen decisions

The specification also defines four explicit forbidden shortcuts:
1. Invoking Lever before Trace has attempted smallest-sufficient handling
2. Jumping to cross-family reroute when a legal local intervention remains
3. Using Residue as a substitute for explicit evaluator adjudication
4. Calling Lever directly for Residue-domain signals (misfit, absence, tension, warp, offset) without first dispatching to Residue

The question: should these rules be **documentation-only** (conventions that agents and callers are expected to honour) or **structurally enforced** (checked before transitions execute)?

---

## Decision

Enforce the trigger ownership model at the runtime boundary via a **PRE_TRANSITION hook** (`hooks/trigger_ownership.py`) registered in the `HookRegistry` and fired by `TransitionEngine` before every high-impact transition.

The hook inspects the pending transition decision — populated in `HookContext.context` by `TransitionEngine._fire_pre_transition` — and blocks violations before they reach the state mutation layer.

### What fires the hook

`TransitionEngine.execute()` fires `PRE_TRANSITION` hooks for:
- `AUTHORITY_CALL` (Trace, Lever, or Residue)
- `CROSS_FAMILY_REROUTE`
- `SIBLING_SHIFT`
- `FORENSICS_RESET`

`CONTINUE` and `PHASE_PIVOT` do not fire `PRE_TRANSITION` — they are low-impact and do not involve authority dispatch.

### What the hook checks

| Rule | Check | Block condition |
|---|---|---|
| Lever after Trace | `_authority_trace_evaluation` in state artifacts or `trace_consulted: true` in context | Lever called with no trace evidence |
| No Residue-as-adjudicator | Adjudication artifacts present while Residue called with non-Residue signal | `contradictions_detected`, `support_gap`, etc. in state + non-Residue signal |
| No premature cross-family reroute | Trust collapse confirmed | `local_pivot_available` in context while no collapse indicators |
| Residue-domain signals through Residue first | `_authority_residue_recommendation` in artifacts or `residue_consulted: true` | Lever called for `misfit_detected`, `absence_detected`, etc. without prior Residue dispatch |

### Context population

`TransitionEngine._fire_pre_transition()` populates the hook context with:

```python
{
    "pending_action": decision.action.value,   # e.g. "authority_call"
    "pending_target": decision.target,          # e.g. "authority:Lever"
    "pending_trigger": decision.trigger,        # trigger ID that caused this
    "pending_authority_data": decision.authority_data or {},
}
```

---

## Options Considered

### Option A: Documentation-only (rejected)

Keep trigger_patterns.md as a specification document that agents and callers are expected to honour, with no runtime enforcement.

| Dimension | Assessment |
|---|---|
| Overhead | None — no additional runtime layer |
| Reliability | Zero — any caller can violate the hierarchy silently |
| Debuggability | Poor — violations produce no structured error; only wrong outputs |
| Drift risk | High — future changes to trigger_patterns.md may not propagate to callers |

**Pros:** No implementation cost.
**Cons:** The ownership hierarchy becomes aspirational rather than contractual. A caller that invokes Lever directly for `misfit_detected` will silently bypass lens-based first response and get a generic evaluator output. The failure is not observable as a violation.

### Option B: Compile-time checks (rejected)

Enforce the hierarchy at pipeline spec parse time — validate that pipeline YAML files only declare authority targets in the correct order.

| Dimension | Assessment |
|---|---|
| Overhead | Moderate — spec validation at load time |
| Reliability | Partial — only catches statically declared sequences; dynamic callers bypass |
| Coverage | Low — imperative code in executors can still call authorities in any order |

**Pros:** Catches spec-level violations early.
**Cons:** Executors and runtime callers are not spec files. A Forge executor that dynamically constructs a `RouteDecision(action=AUTHORITY_CALL, target="authority:Lever")` with no prior Trace dispatch would not be caught.

### Option C: PRE_TRANSITION runtime hook (selected)

| Dimension | Assessment |
|---|---|
| Overhead | One hook evaluation per high-impact transition (negligible) |
| Reliability | Structural — fires before state mutation; violations halt execution with a descriptive error |
| Coverage | All transitions routed through TransitionEngine |
| Debuggability | Violations produce a `HookResult.halt` with a specific rule name and fix guidance |
| Drift risk | Low — hook reads from artifacts and context; stays current with execution state |

**Pros:** Rule violations are caught at the boundary, with named violations and actionable error messages. State is never mutated after a violation. Hook rules are co-located with the trigger_patterns.md spec they enforce.

**Cons:** Requires callers that legitimately bypass the hierarchy (e.g., tests that mock Trace) to explicitly signal `trace_consulted: true` in context. This is a small but real ergonomic cost.

---

## Trade-off Analysis

The main trade-off is **false positive risk** vs. **violation detectability**.

The hook has two safety valves to prevent false positives:
1. Callers can set `trace_consulted: true` in context to signal Trace was consulted via a path that doesn't produce an `_authority_trace_evaluation` artifact (e.g., the evaluation was inlined rather than dispatched)
2. `CONTINUE` and `PHASE_PIVOT` transitions don't fire the hook at all — only high-impact transitions do

The acceptable risk: a test or caller that does not set `trace_consulted: true` and calls Lever directly will get a `HookResult.halt`. This is the correct outcome — it surfaces a real violation that would otherwise produce a wrong output.

---

## Consequences

**Becomes easier:**
- Detecting authority ordering violations during development (fail fast, descriptive error)
- Auditing authority dispatch sequences in state artifacts
- Adding new ownership rules without changing caller code (extend the hook, not the callers)

**Becomes harder:**
- Writing integration tests that call Lever directly without first calling Trace (must set `trace_consulted: true`)
- Using TransitionEngine in lightweight contexts where no hook registry is needed (hook_registry parameter is optional; no-op when None)

**Will need to revisit:**
- Depth limits on Trace→Lever→Trace recursive chains (not yet bounded)
- Whether `PRE_ROUTE` and `POST_TRANSITION` hooks should be wired in the same pattern
- Adding `trigger` as a first-class field on `RouteDecision` (currently read via `getattr(decision, "trigger", "")`)

---

## Action Items

- [x] `hooks/trigger_ownership.py` implemented with four ownership rules
- [x] `trigger_ownership_hook` registered in `RuntimeDispatcher._build_hook_registry()` for `PRE_TRANSITION` at priority 15
- [x] `TransitionEngine._fire_pre_transition()` populates pending_action/target/trigger/authority_data
- [x] `TransitionEngine.__init__` accepts optional `hook_registry` parameter (backward compatible)
- [ ] Add `trigger` as a typed field on `RouteDecision` dataclass (currently relies on `getattr` fallback)
- [ ] Tests for all four ownership rules in `tests/runtime/test_trigger_ownership.py`
- [ ] Wire `hook_registry` injection into TransitionEngine from RuntimeDispatcher when TransitionEngine is used within dispatcher execution flow

---

## References

- `docs/implementation/trigger_patterns.md` — trigger ownership specification
- `hooks/trigger_ownership.py` — implementation
- `runtime/execution/transitions.py` — `_fire_pre_transition` and hook wiring
- `runtime/execution/dispatcher.py` — hook registry construction
- ADR-001 — authority architecture context
