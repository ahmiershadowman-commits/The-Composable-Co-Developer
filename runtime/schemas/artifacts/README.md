# Artifact Schemas

## Purpose

This directory contains YAML schemas defining the structure of all artifacts produced by the marketplace runtime.

## Artifact Categories

### Primary Artifacts

Core artifacts required for handoff and provenance:

| Artifact | Schema | Produced By |
|----------|--------|-------------|
| inventory_ledger | `inventory_ledger.yaml` | Forensics/project_mapping |
| trust_assessment | `trust_assessment.yaml` | All Forensics pipelines |
| route_decision | `route_decision.yaml` | All pipelines |
| canonical_structure_map | `canonical_structure_map.yaml` | Forensics/defragmentation |

### Supporting Artifacts

Contextual artifacts that aid understanding:

| Artifact | Schema | Produced By |
|----------|--------|-------------|
| fragmentation_snapshot | N/A | Forensics/defragmentation |
| audit_report | N/A | Forensics/documentation_audit |
| anomaly_catalog | N/A | Forensics/anomaly_disambiguation |

## Schema Format

Each schema file defines:

```yaml
artifact_name:
  type: object | array | string | number
  required: true | false
  description: Human-readable description
  properties:
    field_name:
      type: ...
      description: ...
      example: ...
```

## Usage

Schemas are used for:

1. **Validation**: Ensure artifacts match expected structure
2. **Documentation**: Clarify artifact contents
3. **Type hints**: Guide executor implementation
4. **Testing**: Verify artifact production

## Artifact Naming

Artifacts use snake_case naming:
- `inventory_ledger` ✅
- `inventoryLedger` ❌

## Artifact Immutability

Once added to state, artifacts cannot be modified:

```python
state.add_artifact("name", data)  # OK
state.artifacts["name"] = new_data  # NOT ALLOWED
```

## Provenance Tracking

All artifacts include provenance metadata:

```yaml
artifact:
  content: {...}
  provenance:
    pipeline: "Forensics/project_mapping"
    phase: "inventory_artifacts"
    timestamp: "2026-03-25T10:30:00Z"
    family: "FORENSICS"
```
