# Provenance Schema

Schema for artifact provenance tracking.

## Structure

```yaml
provenance:
  artifact_name: "inventory_ledger"
  pipeline: "Forensics/project_mapping"
  phase: "inventory_artifacts"
  family: "FORENSICS"
  created_at: "2026-03-25T10:30:00Z"
  
  execution_context:
    session_id: "session_12345"
    trace_id: "trace_abcde"
  
  source_artifacts:
    - "scope_note"
  
  transformations:
    - type: "extract"
      description: "Extracted file inventory from scope"
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `artifact_name` | string | Yes | Name of artifact |
| `pipeline` | string | Yes | Producing pipeline |
| `phase` | string | Yes | Producing phase |
| `family` | string | Yes | Family name |
| `created_at` | string | Yes | ISO timestamp |
| `execution_context` | object | No | Execution identifiers |
| `source_artifacts` | array | No | Input artifacts |
| `transformations` | array | No | Applied transformations |

## Usage

Every artifact written by the runtime includes provenance:

```yaml
# runtime_output/Forensics/project_mapping/inventory_ledger.yaml
content:
  # Artifact data here
_provenance:
  artifact_name: "inventory_ledger"
  pipeline: "Forensics/project_mapping"
  phase: "inventory_artifacts"
  family: "FORENSICS"
  created_at: "2026-03-25T10:30:00Z"
```

## Example

```yaml
provenance:
  artifact_name: "route_recommendation"
  pipeline: "Forensics/project_mapping"
  phase: "recommend_route"
  family: "FORENSICS"
  created_at: "2026-03-25T10:35:00Z"
  execution_context:
    session_id: "session_001"
    trace_id: "trace_xyz"
  source_artifacts:
    - "inventory_ledger"
    - "physical_dependency_graph"
    - "discrepancy_ledger"
    - "trust_zone_map"
  transformations:
    - type: "synthesize"
      description: "Synthesized route from all analysis artifacts"
```
