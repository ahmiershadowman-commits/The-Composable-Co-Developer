# Operators

## Purpose

Operators are cognitive transformations that apply structured work patterns to bounded input state and return structured outputs. They are stronger than primitives but don't replace full pipeline methodology.

## Design Rules

1. **Add robustness more than complexity**: Operators must provide clear value
2. **Callable across families**: Operators work wherever their shape generalizes
3. **Don't replace methodology**: Operators supplement, not replace, pipeline logic
4. **Publish inputs/outputs/failure modes**: Clear contracts for all operators

## Operator Classes

### Local Reading (Band 2)

Extract and parse local information.

**Examples**:
- `source_extract` - Pull content from sources
- `claim_parse` - Extract claims from text
- `dependency_slice` - Map dependencies
- `code_surface_read` - Surface code structure

**Use when**: More than a primitive is needed but phase and family still fit.

---

### Local Transformation (Band 2)

Apply bounded local changes.

**Examples**:
- `rewrite_local_structure` - Reorganize local content
- `metadata_normalize` - Standardize metadata
- `evidence_reweight` - Adjust evidence weights
- `branch_prune` - Remove unnecessary branches

**Use when**: Bounded local change can restore progress.

---

### Bounded Evaluation (Band 4)

Apply specific evaluation criteria.

**Examples**:
- `contradiction_check` - Detect contradictions
- `support_check` - Assess evidence support
- `shape_check` - Verify artifact structure
- `trust_check` - Assess trustworthiness

**Use when**: Trace has identified a need for stronger discrimination.

---

### Synthesis (Band 7)

Create higher-order coherence from accumulated material.

**Examples**:
- `handoff_synthesis` - Create handoff document
- `branch_integration` - Merge divergent branches
- `findings_compression` - Condense findings
- `documentation_reconciliation` - Align documentation

**Use when**: Accumulated material needs higher-order coherence.

---

### Recovery (Band 5)

Restore coherence without full family reroute.

**Examples**:
- `canonical_candidate_selection` - Select best canonical source
- `residue_disposition` - Handle fragmented residue
- `rollback_anchor_resolution` - Rollback to trusted state

**Use when**: Entropy or drift is primary but full family reroute is not yet required.

---

## Available Operators

| Operator | Class | Description |
|----------|-------|-------------|
| `clarify` | local_transformation | Make unclear concepts precise |
| `distill` | local_transformation | Extract essential elements |
| `compare` | bounded_evaluation | Identify similarities and differences |
| `extract` | local_reading | Pull out specific information |
| `reframe` | local_transformation | Shift perspective |
| `triangulate` | bounded_evaluation | Cross-reference multiple sources |

---

## Response Contract

All operators must return:

```yaml
recommended_next_move: string
intervention_band: number
residue_to_preserve: object
```

Operators may also return:

```yaml
generated_artifacts: object
escalation_recommendation: string
route_recommendation: object
```

---

## Usage in Pipelines

Operators are referenced in pipeline specs:

```yaml
smallest_sufficient_interventions:
  operators:
    - distill
    - clarify
```

---

## Relationship to Other Layers

| Layer | Relationship |
|-------|-------------|
| Primitives | Operators may use primitives internally |
| Evaluators | Operators transform; evaluators assess |
| Motifs | Motifs may suggest operator application |
| Trace | Trace may select operators as interventions |

---

## Best Practices

### For Operator Authors

1. **Define clear inputs**: Specify what the operator consumes
2. **Define clear outputs**: Specify what the operator produces
3. **Document failure modes**: When does the operator fail?
4. **Test across families**: Verify operator works in multiple contexts

### For Pipeline Designers

1. **Select operators carefully**: Only include when they add value
2. **Combine with primitives**: Operators often work with primitives
3. **Don't overuse**: 1-2 operators per pipeline is typical
4. **Test empirically**: Verify operators improve outcomes
