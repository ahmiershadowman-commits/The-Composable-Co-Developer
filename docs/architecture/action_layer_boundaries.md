# Action Layer Boundaries

## Purpose

This document defines clear boundaries between primitives, operators, evaluators, and motifs to prevent layer bleed and maintain architectural clarity.

## Layer Definitions

### Motifs (Inference Layer)

**Purpose**: Semantic conditioning patterns that influence attention

**What they do**:
- Detect structural patterns in context
- Modulate attention toward important features
- Suggest (not trigger) interventions

**What they don't do**:
- Execute actions
- Modify state
- Make decisions

**Example**: `unfinished-proof` detects reasoning gaps

---

### Primitives (Action Layer - Atomic)

**Purpose**: Atomic metacognitive and reasoning actions

**What they do**:
- Execute single, focused actions
- Modify state minimally
- Return immediate results

**What they don't do**:
- Combine multiple actions
- Make complex decisions
- Evaluate outcomes

**Categories**:
- **Metacognitive**: `hold`, `locate`, `open`, `shift`, `trim`, `center`, `release`
- **Reasoning**: `bind`, `press`, `reread`, `separate`, `weave`

**Example**: `locate` finds a specific artifact or information

---

### Operators (Action Layer - Transformative)

**Purpose**: Transform understanding or representation

**What they do**:
- Apply cognitive transformations
- Combine multiple primitives internally
- Produce new perspectives

**What they don't do**:
- Evaluate quality of transformations
- Make commitment decisions
- Execute full pipeline phases

**Available operators**:
- `clarify`: Make unclear concepts precise
- `distill`: Extract essential elements
- `compare`: Identify similarities and differences
- `extract`: Pull out specific information
- `reframe`: Shift perspective
- `triangulate`: Cross-reference multiple sources

**Example**: `distill` extracts core requirements from verbose discussion

---

### Evaluators (Assessment Layer)

**Purpose**: Assess quality, validity, or commitment readiness

**What they do**:
- Apply evaluation criteria
- Return judgments (pass/fail/uncertain)
- Recommend next actions

**What they don't do**:
- Execute transformations
- Modify state directly
- Make final commitments (that's Lever)

**Available evaluators**:
- `support_evaluator`: Assess evidence quality
- `contradiction_evaluator`: Detect real vs apparent contradictions
- `discriminator_evaluator`: Identify what distinguishes options
- `frame_evaluator`: Assess framing adequacy
- `artifact_shape_evaluator`: Verify artifact structure
- `trust_evaluator`: Assess trustworthiness

**Example**: `support_evaluator` rates evidence quality as strong/weak/absent

---

## Boundary Rules

### Rule 1: Motifs Don't Trigger

Motifs signal; they don't trigger actions.

**Correct**:
```
Motif detected → Trace recognizes → Trace selects primitive
```

**Incorrect**:
```
Motif detected → Primitive executes automatically ❌
```

### Rule 2: Primitives Are Atomic

Primitives do one thing only.

**Correct**:
```
`locate` finds one thing
`bind` connects two things
```

**Incorrect**:
```
`locate_and_bind` does both ❌
```

### Rule 3: Operators Transform, Not Evaluate

Operators change representation; they don't judge quality.

**Correct**:
```
`distill` → produces distilled version
Then `support_evaluator` → assesses quality
```

**Incorrect**:
```
`distill` → returns "good distillation" ❌
```

### Rule 4: Evaluators Don't Modify State

Evaluators assess; they don't change state.

**Correct**:
```
Evaluator returns judgment → Trace decides action
```

**Incorrect**:
```
Evaluator modifies state.artifacts ❌
```

### Rule 5: Layers Stack, Don't Skip

Interventions stack through layers:

```
Motif (signal) → Primitive (action) → Operator (transform) → Evaluator (assess)
```

Don't skip layers:
```
Motif → Evaluator (skips action/transform) ❌
```

---

## Decision Tree

When designing an intervention, use this tree:

```
Does it detect patterns without acting?
├─ Yes → MOTIF
└─ No → Does it execute a single atomic action?
    ├─ Yes → PRIMITIVE
    └─ No → Does it transform understanding?
        ├─ Yes → OPERATOR
        └─ No → Does it assess quality?
            ├─ Yes → EVALUATOR
            └─ No → Not an intervention (pipeline or method)
```

---

## Examples by Layer

### Motif Examples

| Motif | Detects | Signals |
|-------|---------|---------|
| `unfinished-proof` | Reasoning without support | Evidence gap |
| `watershed` | High-stakes decision point | Need for criteria |
| `tension_point` | Conflicting claims | Need for resolution |
| `absence_signal` | Missing expected content | Need for investigation |

### Primitive Examples

| Primitive | Does | Returns |
|-----------|------|---------|
| `locate` | Finds specific item | Item location |
| `hold` | Maintains current state | Continuation signal |
| `separate` | Distinguishes items | Separation result |
| `bind` | Connects items | Connection result |

### Operator Examples

| Operator | Transforms | Output |
|----------|------------|--------|
| `clarify` | Unclear → Clear | Clarified concept |
| `distill` | Verbose → Essential | Core elements |
| `compare` | Two items → Comparison | Similarity/difference map |
| `reframe` | Frame A → Frame B | New perspective |

### Evaluator Examples

| Evaluator | Assesses | Returns |
|-----------|----------|---------|
| `support_evaluator` | Evidence quality | Strong/weak/absent |
| `contradiction_evaluator` | Claim conflict | Real/apparent/none |
| `discriminator_evaluator` | Option differences | Key discriminators |
| `artifact_shape_evaluator` | Artifact structure | Valid/invalid |

---

## Common Violations

### Violation 1: Operator Doing Evaluation

**Bad**:
```yaml
clarify:
  description: Clarify and validate concept
  # ❌ "validate" is evaluation, not transformation
```

**Good**:
```yaml
clarify:
  description: Make unclear concept precise
  # ✅ Pure transformation
# Then use support_evaluator separately
```

### Violation 2: Primitive Doing Multiple Actions

**Bad**:
```yaml
locate_and_analyze:
  description: Find artifact and analyze content
  # ❌ Two actions in one primitive
```

**Good**:
```yaml
locate:
  description: Find specific artifact
# Then use separate operator for analysis
```

### Violation 3: Evaluator Modifying State

**Bad**:
```python
def evaluate_support(evidence):
    state.artifacts['evaluation'] = 'strong'  # ❌ Modifies state
    return 'strong'
```

**Good**:
```python
def evaluate_support(evidence):
    return {'judgment': 'strong'}  # ✅ Returns judgment only
```

### Violation 4: Motif Triggering Action

**Bad**:
```yaml
unfinished-proof:
  on_detect:
    execute: primitive:bind  # ❌ Motifs don't trigger
```

**Good**:
```yaml
unfinished-proof:
  related_interventions:
    primitives: [bind]  # ✅ Suggests, doesn't trigger
```

---

## Testing Boundaries

### Boundary Test Questions

For any intervention, ask:

1. **Motif test**: Does it only detect patterns without acting?
2. **Primitive test**: Does it do exactly one atomic action?
3. **Operator test**: Does it transform without evaluating?
4. **Evaluator test**: Does it assess without modifying?

If any answer is "no", the intervention violates boundaries.

### Refactoring Violations

When violations are found:

1. **Split multi-action primitives** into separate primitives
2. **Extract evaluation from operators** into separate evaluators
3. **Remove state modification from evaluators**
4. **Remove triggering from motifs**

---

## Summary Table

| Layer | Purpose | Modifies State? | Makes Decisions? | Example |
|-------|---------|-----------------|------------------|---------|
| Motif | Pattern detection | No | No | `unfinished-proof` |
| Primitive | Atomic action | Yes (minimal) | No | `locate` |
| Operator | Transformation | Yes | No | `distill` |
| Evaluator | Assessment | No | No (recommends) | `support_evaluator` |
