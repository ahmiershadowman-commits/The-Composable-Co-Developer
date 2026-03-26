# Authority Escalation Trace

## Purpose

This worked trace demonstrates the full authority escalation chain: Trace → Residue → Lever → Commitment.

## Trace Overview

**Route**: Trace (routine) → Residue (anomaly detected) → Lever (evaluator) → Commitment

**Scenario**: Contradiction detected between two architectural claims requires adjudication.

---

## Step 1: Trace Evaluation (Routine)

**Entry condition**: Normal pipeline execution, trust established

**State**:
```yaml
current_pipeline: Forge/development
trust_assessment:
  trust_level: high
  canonical_sources_identified: true
```

**Trace evaluates**:
- Trust assessment: high
- State: stable
- No immediate issues

**Initial route decision**: Continue to Forge/coding

---

## Step 2: Residue Detection (Anomaly)

**Trigger**: Trace detects suspicious surface during evaluation

**Anomaly signal**: tension_detected

**Residue consulted**:
```yaml
lens: tension
state:
  claim_a: "System must be real-time"
  claim_b: "Batch processing is acceptable"
```

**Residue applies lens**:
- Detects conflicting constraints
- Identifies stakeholder divergence
- Notes trade-off not acknowledged

**Residue interpretation**:
```yaml
tension_type: competing_constraints
severity: high
stakeholders:
  - ops_team (real-time)
  - data_team (batch)
```

**Trace incorporates interpretation**:
- Recognizes contradiction requires adjudication
- Smallest sufficient intervention insufficient
- Escalation to Lever required

---

## Step 3: Lever Escalation

**Entry condition**: Trace escalated, evaluator needed

**Lever receives**:
```yaml
escalation_reason: contradiction_requires_adjudication
context:
  claim_a: "System must be real-time"
  claim_b: "Batch processing is acceptable"
  tension_analysis: {...}
```

**Lever selects evaluator**:
```yaml
evaluator: contradiction_evaluator
rationale: "Real vs apparent contradiction must be determined"
```

**Evaluator executes**:
```yaml
contradiction_analysis:
  type: apparent
  explanation: "Claims operate at different abstraction levels"
  resolution_path: "Clarify scope of real-time requirement"
```

**Lever makes commitment decision**:
```yaml
decision: reopen
rationale: "Contradiction is apparent, not real"
next_action: "Reframe with clarified scope"
```

---

## Step 4: Route Decision (Post-Adjudication)

**Lever produces route**:
```yaml
target: pipeline:Forge/development
reason: "reframe_needed_before_continuation"
confidence: high
```

**State updated**:
- Route history recorded
- Evaluator result documented
- Commitment decision preserved

---

## Authority Interaction Summary

| Authority | Action | Output |
|-----------|--------|--------|
| Trace | Routine evaluation | Initial route decision |
| Trace | Detects anomaly | Consult Residue |
| Residue | Apply tension lens | Interpretation |
| Trace | Incorporate interpretation | Escalate to Lever |
| Lever | Select evaluator | contradiction_evaluator |
| Evaluator | Analyze contradiction | Apparent, not real |
| Lever | Make decision | Reopen, reframe needed |

---

## Key Learnings

1. **Trace first**: Routine evaluation always starts with Trace
2. **Residue for anomalies**: Suspicious surface → Residue lens
3. **Lever for adjudication**: Contradictions require evaluator
4. **Proper escalation order**: Trace → Residue → Lever (not skipped)

---

## Forbidden Patterns Avoided

- ❌ Lever before Trace (skipping smallest-sufficient)
- ❌ Residue as pipeline family (Residue is authority, not family)
- ❌ Residue making commitment decision (that's Lever's role)

---

## Validation Checklist

- [x] Trace evaluated first (always)
- [x] Residue consulted for anomaly interpretation
- [x] Lever escalated only after Trace determined insufficiency
- [x] Evaluator selected appropriately (contradiction_evaluator)
- [x] Commitment decision made by Lever, not Residue

---

## Trace File

Location: `examples/worked_traces/authority_escalation_trace.md`

Test: `tests/worked_examples/test_authority_escalation_trace.py`
