# Artifact Contract

## Purpose

This document defines the contract for artifact production, structure, and usage across the marketplace runtime.

## Artifact Definition

An **artifact** is any structured data product generated during pipeline execution.

### Characteristics

- **Named**: Each artifact has a unique identifier within a pipeline
- **Structured**: Follows defined schema (YAML or JSON)
- **Immutable**: Cannot be modified after creation
- **Provenanced**: Tracks which pipeline/phase produced it

## Artifact Lifecycle

```
Created → Added to State → Written to Disk → Archived
    ↑           ↑               ↑              ↑
  Phase     Executor      ArtifactWriter   SessionEnd
  complete
```

## Production Rules

### 1. Phase Output Rule

Each phase produces exactly one primary artifact:

```yaml
phase_contracts:
  inspect_state:
    outputs:
      - fragmentation_snapshot  # Exactly one primary
```

### 2. Naming Rule

Artifact names must be:
- snake_case format
- Unique within pipeline
- Descriptive of content
- Max 50 characters

**Valid**: `inventory_ledger`, `trust_reassessment_note`
**Invalid**: `inventoryLedger`, `data1`, `stuff`

### 3. Schema Rule

All artifacts must conform to their schema:

```python
# Schema validation happens at add time
state.add_artifact("inventory_ledger", data)  # Validates against schema
```

### 4. Provenance Rule

All artifacts include provenance:

```yaml
artifact:
  content: {...}
  _provenance:
    pipeline: "Forensics/project_mapping"
    phase: "inventory_artifacts"
    timestamp: "2026-03-25T10:30:00Z"
    family: "FORENSICS"
```

## Artifact Categories

### Primary Artifacts

Required for pipeline exit conditions:

```yaml
exit_conditions:
  - inventory_ledger_present
  - route_recommendation_present
```

**Characteristics**:
- Listed in pipeline spec `artifacts.primary`
- Required for exit
- Validated before completion

### Supporting Artifacts

Contextual but not required:

```yaml
artifacts:
  supporting:
    - fragmentation_snapshot
```

**Characteristics**:
- Aid understanding
- Not required for exit
- May be omitted in edge cases

## Artifact Update Semantics

### Add (Only Operation)

Artifacts can only be added, not modified:

```python
state.add_artifact("name", data)  # OK
state.artifacts["name"] = other   # ERROR
state.artifacts.pop("name")       # ERROR
```

### Rationale

Immutability ensures:
- **Audit trail**: History is preserved
- **Debugging**: Can trace what changed
- **Reproducibility**: Same input → same output

## Artifact Access

### Reading Artifacts

```python
# From state
artifact = state.artifacts.get("name")

# Check existence
if "name" in state.artifacts:
    ...
```

### Artifact Dependencies

Later phases can depend on earlier artifacts:

```yaml
phase_contracts:
  verify_coherence:
    depends_on:
      - residue_disposition_ledger
      - metadata_normalization_record
```

## Artifact Validation

### Schema Validation

Artifacts are validated against schemas:

```python
def add_artifact(self, name: str, data: Any):
    schema = self._get_schema(name)
    validate(data, schema)  # Raises if invalid
    self.artifacts[name] = data
```

### Content Validation

Beyond schema, artifacts must be:
- Non-empty (unless empty is meaningful)
- Internally consistent
- Consistent with prior artifacts

## Artifact Output

### File Format

Artifacts written as YAML:

```yaml
# runtime_output/pipeline_artifact_name.yaml
content:
  # Artifact data
_provenance:
  pipeline: "..."
  phase: "..."
  timestamp: "..."
```

### Directory Structure

```
runtime_output/
├── Forensics/
│   ├── project_mapping/
│   │   ├── inventory_ledger.yaml
│   │   └── route_recommendation.yaml
│   └── defragmentation/
│       └── canonical_structure_map.yaml
```

## Artifact Contracts by Family

### Forensics Artifacts

| Pipeline | Primary Artifacts |
|----------|------------------|
| project_mapping | inventory_ledger, physical_dependency_graph, discrepancy_ledger, trust_zone_map, canonical_source_note, route_recommendation |
| defragmentation | fragmentation_snapshot, entropy_classification, chosen_method, residue_disposition_ledger, changed_structure_map, metadata_normalization_record, trust_reassessment_note, route_recommendation |
| documentation_audit | documentation_inventory, code_state_inventory, drift_ledger, gap_analysis, misleading_claims_ledger, audit_report, route_recommendation |
| anomaly_disambiguation | anomaly_catalog, anomaly_classification, disambiguation_options, recommended_path, route_recommendation |

### Forge Artifacts

| Pipeline | Primary Artifacts |
|----------|------------------|
| development | problem_frame, architecture_note, work_plan, slice_map, verification_summary, route_recommendation |
| coding | change_understanding, change_plan, changed_artifact, validation_note, route_recommendation |
| testing | test_scope, test_strategy, test_results, test_report, route_recommendation |
| refactor | current_shape_map, invariants_ledger, refactor_plan, refactored_artifact, behavior_validation, route_recommendation |

### Inquiry Artifacts

| Pipeline | Primary Artifacts |
|----------|------------------|
| research | question_frame, source_ledger, comparison_map, synthesis_note, support_and_gap_map, route_recommendation |
| hypothesis_generation | phenomenon_description, candidate_set, discriminator_list, provisional_selection_note, evidence_gap_note, route_recommendation |
| formalization | concept_packet, object_relation_map, assumption_ledger, definition_set, notation_sheet, route_recommendation |
| mathematics | problem_statement, assumptions_ledger, derivation_record, edge_case_notes, rigor_assessment, result_artifact, route_recommendation |

### Conduit Artifacts

| Pipeline | Primary Artifacts |
|----------|------------------|
| documentation | audience_scope_note, source_packet, structure_outline, draft_document, support_note, metadata_update_record, route_recommendation |
| handoff_synthesis | handoff_scope_note, handoff_source_packet, core_structure_map, handoff_document, unresolveds_and_risks, provenance_summary, next_safe_steps |
| professional_writing | audience_objective_statement, outline, draft_document, refinement_log, validation_note, delivery_record |
| scholarly_writing | genre_frame, source_packet, outline, claim_hierarchy, draft, citation_map, final_document |

## Error Handling

### Missing Required Artifact

If a required artifact is not produced:

1. Phase marked as failed
2. Error recorded in state
3. Pipeline halts
4. Route to Forensics for investigation

### Invalid Artifact Schema

If artifact doesn't match schema:

1. Validation error raised
2. Artifact not added to state
3. Phase marked as failed
4. Executor must fix and retry

## Best Practices

### For Executor Authors

1. **Produce artifacts in phase order**
2. **Validate before adding**: Check data quality
3. **Use descriptive names**: `inventory_ledger` not `data1`
4. **Include all required fields**: Check schema
5. **Document deviations**: If artifact differs from schema

### For Pipeline Designers

1. **One artifact per phase**: Clear mapping
2. **Name artifacts consistently**: Follow conventions
3. **Specify schemas**: Don't leave structure ambiguous
4. **Test artifact production**: Verify in worked traces
