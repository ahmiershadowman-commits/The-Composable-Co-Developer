# Method Target Legality

## Purpose

This document defines the legality rules for `method:<name>` targets within the runtime target grammar.

## Canonical Target Grammar

The runtime recognizes these target types:

```
pipeline:<Family>/<id>
family:<Family>
primitive:<name>
operator:<name>
evaluator:<name>
method:<name>
authority:<Trace|Lever|Residue>
forensics_reset
```

## Method Target Definition

### What Is a Method?

A `method` is an internal sub-pipeline operation used within defragmentation and other complex pipelines.

**Examples**:
- `method:tidy`
- `method:consolidate`
- `method:repair`
- `method:anchor`

### Legality Rules

#### Rule 1: Pipeline-Scoped Only

Methods are ONLY valid within the pipeline that declares them.

**Legal**:
```yaml
# Inside Forensics/defragmentation pipeline
pivot_conditions:
  canonical_conflict_unresolved:
    action: phase_pivot
    target: method:anchor  # ✅ Legal - anchor is declared in this pipeline
```

**Illegal**:
```yaml
# Inside Forensics/project_mapping pipeline
route_recommendation:
  target: method:anchor  # ❌ Illegal - anchor not declared in this pipeline
```

#### Rule 2: Must Be Declared in internal_methods

Methods must be explicitly declared in the pipeline spec:

```yaml
internal_methods:
  tidy:
    use_when:
      - minor_residue
      - naming_drift
  # ... other methods
```

Methods not declared in `internal_methods` cannot be targeted.

#### Rule 3: Phase Pivot Action Only

Methods can only be targeted via `phase_pivot` action:

**Legal**:
```yaml
action: phase_pivot
target: method:repair
```

**Illegal**:
```yaml
action: reroute
target: method:tidy  # ❌ Illegal - reroute cannot target methods
```

#### Rule 4: Cannot Cross Pipeline Boundary

Methods cannot be targeted from outside their pipeline:

**Legal**:
```yaml
# Inside defragmentation pipeline
target: method:consolidate  # ✅ Legal - same pipeline
```

**Illegal**:
```yaml
# Inside project_mapping pipeline
target: method:consolidate  # ❌ Illegal - different pipeline
```

#### Rule 5: Cannot Be External Target

Methods cannot be route recommendations:

**Legal**:
```yaml
route_recommendation:
  target: family:Forge  # ✅ Legal - external target
```

**Illegal**:
```yaml
route_recommendation:
  target: method:anchor  # ❌ Illegal - methods are internal only
```

---

## Validation Logic

### Target Resolver Method Validation

```python
def validate_method_target(target: str, current_pipeline: PipelineSpec) -> bool:
    # Extract method name
    method_name = target.replace("method:", "")
    
    # Check if method is declared in current pipeline
    if method_name not in current_pipeline.internal_methods:
        return False, f"Method {method_name} not declared in {current_pipeline.id}"
    
    # Check if action is phase_pivot
    if current_action != "phase_pivot":
        return False, f"Methods can only be targeted via phase_pivot"
    
    return True, "Valid method target"
```

---

## Method Declaration Format

### Required Fields

```yaml
internal_methods:
  method_name:
    use_when:
      - condition_1
      - condition_2
```

### Optional Fields

```yaml
internal_methods:
  method_name:
    use_when:
      - condition_1
    phase_order:
      - phase_1
      - phase_2
    artifacts:
      - artifact_name
```

---

## Current Method Inventory

### Forensics/defragmentation

| Method | Purpose | Conditions |
|--------|---------|------------|
| `tidy` | Minor cleanup | `minor_residue`, `naming_drift`, `lightweight_metadata_disorder` |
| `consolidate` | Merge duplicates | `overlapping_artifacts`, `multiple_near_canonical_sources` |
| `repair` | Align drifted artifacts | `project_shape_has_drifted`, `code_spec_docs_disagree` |
| `anchor` | Rollback/recovery | `no_trustworthy_canonical`, `severe_fragmentation` |

---

## Error Messages

### Method Not Declared

```
Error: Method 'method:unknown' is not declared in pipeline 'Forensics/defragmentation'
Declared methods: tidy, consolidate, repair, anchor
```

### Method Cross-Pipeline

```
Error: Cannot target 'method:tidy' from pipeline 'Forensics/project_mapping'
Methods are internal to their declaring pipeline
```

### Method Wrong Action

```
Error: Method 'method:anchor' cannot be targeted with action 'reroute'
Methods can only be targeted with action 'phase_pivot'
```

---

## Design Rationale

### Why Methods Are Pipeline-Scoped

1. **Encapsulation**: Each pipeline defines its own internal operations
2. **Clarity**: No ambiguity about which methods are available
3. **Safety**: Prevents accidental cross-pipeline method calls
4. **Maintainability**: Changes to methods don't affect other pipelines

### Why Phase Pivot Only

1. **Semantic clarity**: Phase pivot means "try different approach in same phase"
2. **Consistency**: All phase-level decisions use same action type
3. **Validation**: Easier to validate phase_pivot vs reroute

---

## Best Practices

### For Pipeline Designers

1. **Declare all methods**: List every internal method in `internal_methods`
2. **Use descriptive names**: `anchor` is clearer than `method_4`
3. **Document conditions**: Specify when each method should be used
4. **Test method pivots**: Verify method targets resolve correctly

### For Executor Authors

1. **Check method availability**: Verify method is declared before use
2. **Handle method failures**: Gracefully handle unknown methods
3. **Log method selection**: Record which method was chosen and why

---

## Related Documents

- `target_grammar.yaml` - Full target grammar specification
- `pipeline.yaml` - Pipeline spec format including `internal_methods`
- `action_layer_boundaries.md` - Boundaries between intervention types
