# Shared Authority Execution Order

## Purpose

This document explicitly defines the execution order and interaction patterns between the three shared authorities: Trace, Lever, and Residue.

## Authority Roles

### Trace (Metacognitive Controller)

**Responsibility**: Routine micro-checks and smallest-sufficient intervention selection

**When it acts**:
- Before every pipeline execution
- When trust assessment is available
- When state needs routing

**What it does**:
- Evaluates trust + state
- Selects smallest sufficient intervention
- Produces route decisions

**Does NOT do**:
- Complex evaluation (delegates to Lever)
- Suspicious surface interpretation (delegates to Residue)

---

### Residue (Suspicious-Surface Interpreter)

**Responsibility**: Interpret anomalies through investigative lenses

**When it acts**:
- When suspicious surface is detected
- When anomaly signals appear
- When Trace requests lens interpretation

**What it does**:
- Applies lenses (misfit, absence, tension, warp, offset)
- Produces interpretations
- Suggests investigative directions

**Does NOT do**:
- Make commitment decisions
- Replace explicit evaluator adjudication

---

### Lever (Evaluator / Escalation Authority)

**Responsibility**: Evaluator invocation and explicit adjudication

**When it acts**:
- When Trace's smallest-sufficient handling is inadequate
- When Residue interpretation requires adjudication
- When commitment/reopen decisions are needed

**What it does**:
- Invokes evaluators
- Makes adjudication decisions
- Handles escalation

**Does NOT do**:
- Act before Trace has attempted handling
- Substitute for Residue lens interpretation

---

## Execution Order

### Standard Order (Routine Execution)

```
1. Trace evaluates (always first)
   ↓
2. Trace selects intervention
   ↓
3a. If primitive/operator sufficient → Execute
3b. If evaluator needed → Escalate to Lever
3c. If suspicious surface → Consult Residue
```

**Trace is ALWAYS the first authority consulted.**

---

### Escalation Order (When Trace Insufficient)

```
1. Trace evaluates
   ↓
2. Trace determines insufficiency
   ↓
3. Escalate to Lever
   ↓
4. Lever selects evaluator
   ↓
5. Evaluator produces judgment
   ↓
6. Lever makes commitment/reopen decision
```

**Lever is ONLY consulted after Trace has attempted handling.**

---

### Residue Consultation Order

```
1. Trace evaluates
   ↓
2. Trace detects suspicious surface signal
   ↓
3. Consult Residue for lens interpretation
   ↓
4. Residue applies appropriate lens
   ↓
5. Residue returns interpretation
   ↓
6. Trace incorporates interpretation into route decision
```

**Residue is consulted in parallel with or after Trace evaluation, never before.**

---

## Forbidden Orders

### ❌ Lever Before Trace

```
Lever → Trace  # WRONG
```

**Why forbidden**: Trace must attempt smallest-sufficient handling first. Skipping to Lever bypasses the principle of least invasive intervention.

**Correct order**:
```
Trace → (if insufficient) → Lever
```

---

### ❌ Residue as Pipeline Family

```
Residue → Pipeline execution  # WRONG
```

**Why forbidden**: Residue is an authority, not a family. It provides lens interpretation, not pipeline execution.

**Correct usage**:
```
Trace → (detects anomaly) → Residue (lens) → Trace (route decision)
```

---

### ❌ Residue Substitute for Evaluator

```
Residue → Commitment decision  # WRONG
```

**Why forbidden**: Residue interprets; it doesn't adjudicate. Commitment decisions require explicit evaluator adjudication via Lever.

**Correct order**:
```
Residue (interpretation) → Lever (evaluator) → Lever (decision)
```

---

## Trigger-to-Authority Mapping

| Trigger | First Authority | Possible Escalation |
|---------|-----------------|---------------------|
| `phase_mismatch` | Trace | - |
| `confidence_support_mismatch` | Trace | Lever (if primitive insufficient) |
| `branch_sprawl` | Trace | Lever (discriminator_evaluator) |
| `trust_collapse` | Trace | Forensics reroute |
| `artifact_shape_drift` | Trace | Lever (artifact_shape_evaluator) |
| `misfit_detected` | Residue | Trace (route decision) |
| `absence_detected` | Residue | Trace (route decision) |
| `tension_detected` | Residue | Lever (contradiction_evaluator) |
| `contradiction_requires_adjudication` | Lever | - |
| `discriminator_required` | Lever | - |

---

## Interaction Patterns

### Pattern 1: Trace → Residue → Trace

```python
# Trace detects potential anomaly
trace_result = trace.evaluate(state, trust_assessment)

if trace_result.suspicious_surface:
    # Consult Residue for interpretation
    residue_result = residue.apply_lens(state, lens="misfit")
    
    # Trace incorporates interpretation
    final_decision = trace.finalize_decision(residue_result)
```

---

### Pattern 2: Trace → Lever → Commitment

```python
# Trace evaluates
trace_result = trace.evaluate(state, trust_assessment)

if trace_result.requires_evaluator:
    # Escalate to Lever
    lever_result = lever.escalate(
        state,
        evaluator="support_evaluator"
    )
    
    # Lever makes commitment decision
    if lever_result.commitment_ready:
        decision = lever.commit(state)
    else:
        decision = lever.reopen(state)
```

---

### Pattern 3: Residue → Trace → Lever → Commitment

```python
# Residue detects tension
residue_result = residue.apply_lens(state, lens="tension")

# Trace incorporates and determines evaluator needed
trace_result = trace.evaluate_with_residue(state, residue_result)

if trace_result.requires_adjudication:
    # Escalate to Lever for contradiction evaluation
    lever_result = lever.escalate(
        state,
        evaluator="contradiction_evaluator"
    )
    
    # Lever makes decision
    decision = lever.decide(lever_result)
```

---

## Authority Selection Logic

### Trace Selection Criteria

Trace is selected when:
- ✅ Routine routing is needed
- ✅ Trust assessment is available
- ✅ No suspicious surface detected
- ✅ Smallest-sufficient intervention is primitive/operator

---

### Residue Selection Criteria

Residue is selected when:
- ✅ Anomaly signal detected (misfit, absence, tension, warp, offset)
- ✅ Suspicious surface interpretation needed
- ✅ Investigative lens required

---

### Lever Selection Criteria

Lever is selected when:
- ✅ Trace's smallest-sufficient handling is inadequate
- ✅ Explicit evaluator adjudication required
- ✅ Commitment/reopen decision needed
- ✅ Escalation threshold crossed

---

## Implementation in Runtime

### TraceSelector

```python
class TraceSelector:
    def evaluate(self, state, trust_assessment, pipeline_spec):
        # Always first authority consulted
        if trust_assessment.requires_escalation:
            return self._escalate_to_lever(state)
        
        if state.has_suspicious_surface:
            return self._consult_residue(state)
        
        return self._select_intervention(state)
```

---

### ResidueDispatch

```python
class ResidueDispatch:
    def apply_lens(self, state, lens):
        # Only consulted when anomaly detected
        lens_func = self.lens_registry.get(lens)
        if not lens_func:
            raise UnknownLensError(lens)
        
        return lens_func(state)
```

---

### LeverEscalation

```python
class LeverEscalation:
    def escalate(self, state, evaluator):
        # Only consulted after Trace escalation
        evaluator_func = self.evaluator_registry.get(evaluator)
        result = evaluator_func(state)
        
        return self._make_decision(result)
```

---

## Testing Authority Order

### Unit Test Pattern

```python
def test_trace_first():
    """Verify Trace is consulted before Lever."""
    call_order = []
    
    trace = MockTrace(on_evaluate=lambda: call_order.append("trace"))
    lever = MockLever(on_escalate=lambda: call_order.append("lever"))
    
    runtime = Runtime(trace, lever)
    runtime.execute(state)
    
    assert call_order[0] == "trace"
```

---

### Integration Test Pattern

```python
def test_full_escalation_chain():
    """Verify Trace → Residue → Lever → Commitment chain."""
    state = ExecutionState()
    state.add_suspicious_surface("tension_detected")
    
    result = runtime.execute(state)
    
    # Verify full chain executed
    assert "trace_evaluated" in state.metadata
    assert "residue_applied" in state.metadata
    assert "lever_escalated" in state.metadata
    assert "commitment_made" in state.metadata
```

---

## Related Documents

- `trigger_patterns.md` - Full trigger specification
- `action_layer_boundaries.md` - Authority vs intervention layers
- `runtime_execution_semantics.md` - How authorities fit into execution
