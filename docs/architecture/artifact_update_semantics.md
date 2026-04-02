# Artifact Update Semantics

## Purpose

This document defines the semantics for how artifacts can be updated, replaced, appended, merged, or versioned within the marketplace runtime.

## Core Principle: Immutability

**Artifacts are immutable once added to state.**

```python
state.add_artifact("name", data)  # ✅ OK
state.artifacts["name"] = other   # ❌ NOT ALLOWED
state.artifacts.pop("name")       # ❌ NOT ALLOWED
```

## Update Operations

### Add (Only Direct Operation)

The only direct operation is adding a new artifact:

```python
state.add_artifact("inventory_ledger", inventory_data)
```

**Constraints**:
- Name must be unique within pipeline
- Data must conform to schema
- Provenance is automatically added

### Replace (Via New Artifact)

To "replace" an artifact, create a new one with a different name:

```python
# Original
state.add_artifact("draft_v1", draft_data)

# Replacement (new name)
state.add_artifact("draft_v2", revised_draft_data)
```

**Pattern**: Use versioned names for iterative work.

### Append (Via Collection Artifact)

To append to existing data, create a collection artifact:

```python
# First item
state.add_artifact("finding_1", finding_data)

# Collection artifact
state.add_artifact("findings_collection", {
    "findings": [finding_data_1, finding_data_2, finding_data_3]
})
```

**Pattern**: Aggregate items into collection artifacts.

### Merge (Via New Artifact)

To merge multiple artifacts, create a new merged artifact:

```python
# Source artifacts
state.add_artifact("doc_inventory", doc_data)
state.add_artifact("code_inventory", code_data)

# Merged artifact
state.add_artifact("combined_inventory", {
    "documents": doc_data,
    "code": code_data,
    "merged_at": datetime.now().isoformat()
})
```

**Pattern**: Create explicit merge artifacts with provenance.

### Version (Via Naming Convention)

To version artifacts, use naming conventions:

```python
state.add_artifact("design_draft_v1", data_v1)
state.add_artifact("design_draft_v2", data_v2)
state.add_artifact("design_draft_final", final_data)
```

**Pattern**: Use `_vN` suffix for versions, `_final` for final.

---

## Read Patterns

### Latest Version

To get the latest version of a versioned artifact:

```python
def get_latest(state, prefix):
    versions = [k for k in state.artifacts if k.startswith(prefix)]
    if not versions:
        return None
    return max(versions)  # Assumes v1, v2, v3 naming

latest = get_latest(state, "design_draft_v")
```

### All Versions

To get all versions:

```python
def get_all_versions(state, prefix):
    return sorted([k for k in state.artifacts if k.startswith(prefix)])

versions = get_all_versions(state, "design_draft_v")
```

### Merge History

To reconstruct change history:

```python
history = []
for key in sorted(state.artifacts.keys()):
    if key.startswith("draft"):
        history.append({
            "version": key,
            "artifact": state.artifacts[key],
            "provenance": state.artifacts[key].get("_provenance")
        })
```

---

## Pipeline-Specific Semantics

### Forensics Pipelines

**Pattern**: Each phase produces one artifact, no replacement.

```yaml
phase_order:
  - inspect_state      # → fragmentation_snapshot
  - classify_entropy   # → entropy_classification
  - choose_method      # → chosen_method
```

**Rationale**: Forensics creates audit trail; immutability is essential.

### Forge Pipelines

**Pattern**: May produce iteration artifacts with versioned names.

```yaml
# coding pipeline
phase_order:
  - understand_change  # → change_understanding
  - plan_change        # → change_plan_v1
  - implement_change   # → changed_artifact_v1
  # If iteration needed:
  - revise_plan        # → change_plan_v2
  - reimplement        # → changed_artifact_v2
```

**Rationale**: Build work may iterate; versions track progress.

### Inquiry Pipelines

**Pattern**: Build up evidence collections.

```yaml
# research pipeline
phase_order:
  - gather_sources     # → source_ledger
  - compare_perspectives # → comparison_map
  - synthesize         # → synthesis_note_v1
  # If revision needed:
  - revise_synthesis   # → synthesis_note_v2
```

**Rationale**: Understanding deepens; versions show evolution.

### Conduit Pipelines

**Pattern**: Draft → Refine → Final progression.

```yaml
# documentation pipeline
phase_order:
  - outline_structure  # → structure_outline
  - draft              # → draft_document_v1
  - verify_support     # → support_note
  - refine             # → draft_document_v2
  - finalize           # → final_document
```

**Rationale**: Writing is iterative; final artifact is authoritative.

---

## Provenance Tracking

All artifacts include provenance:

```yaml
artifact:
  content: {...}
  _provenance:
    pipeline: "Forensics/project_mapping"
    phase: "inventory_artifacts"
    timestamp: "2026-03-25T10:30:00Z"
    family: "FORENSICS"
    version: 1  # Explicit version if versioned
```

### Provenance for Versions

Versioned artifacts include version in provenance:

```yaml
draft_document_v2:
  content: {...}
  _provenance:
    pipeline: "Conduit/documentation"
    phase: "refine"
    timestamp: "2026-03-25T11:00:00Z"
    version: 2
    supersedes: draft_document_v1
```

---

## State Checkpoint Semantics

### Checkpoint Creation

Checkpoints capture full state including all artifacts:

```python
checkpoint = {
    "state": state.serialize(),
    "artifacts": dict(state.artifacts),
    "route_history": list(state.route_history),
    "timestamp": datetime.now().isoformat()
}
```

### Checkpoint Restoration

Restoring a checkpoint restores all artifacts:

```python
def restore_checkpoint(checkpoint):
    state = ExecutionState.deserialize(checkpoint["state"])
    state.artifacts = checkpoint["artifacts"]
    return state
```

### Immutability Preserved

Even after checkpoint restore, artifacts remain immutable:

```python
state = restore_checkpoint(checkpoint)
state.add_artifact("new_artifact", data)  # ✅ OK
state.artifacts["old_artifact"] = other   # ❌ Still not allowed
```

---

## Error Cases

### Duplicate Name Error

```python
state.add_artifact("inventory", data1)
state.add_artifact("inventory", data2)  # ERROR: Duplicate name
```

**Resolution**: Use different name for second artifact.

### Schema Mismatch Error

```python
state.add_artifact("inventory", {"wrong": "schema"})  # ERROR: Schema mismatch
```

**Resolution**: Ensure data conforms to artifact schema.

### Missing Provenance Error

```python
# This is handled automatically, but if bypassed:
artifact = {"content": {...}}  # Missing _provenance
state.add_artifact("test", artifact)  # ERROR: Missing provenance
```

**Resolution**: Let `add_artifact` handle provenance automatically.

---

## Best Practices

### For Executor Authors

1. **Use unique names**: Each artifact name should be unique within pipeline
2. **Version explicitly**: Use `_v1`, `_v2` suffixes for iterations
3. **Mark final versions**: Use `_final` suffix for authoritative versions
4. **Document naming**: Explain naming conventions in pipeline specs

### For Pipeline Designers

1. **One artifact per phase**: Clear mapping simplifies tracking
2. **Plan for iteration**: Include versioning strategy if iteration expected
3. **Define final artifacts**: Specify which artifacts are authoritative
4. **Test artifact flow**: Verify artifact names don't conflict

---

## Related Documents

- `artifact_contract.md` - Full artifact contract specification
- `unresolveds_ledger.md` - How unresolveds persist across artifacts
- `runtime_execution_semantics.md` - How artifacts fit into execution
