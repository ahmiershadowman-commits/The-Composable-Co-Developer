# Artifact Schemas

Schema definitions for all runtime artifacts.

## Available Schemas

| Schema | Description | Produced by |
|--------|-------------|-------------|
| `inventory_ledger.yaml` | Project file/artifact inventory | Forensics/project_mapping |
| `trust_zone_map.yaml` | Per-area trust classification | Forensics/project_mapping |
| `discrepancy_ledger.yaml` | Doc vs. observed state conflicts | Forensics/project_mapping, documentation_audit |
| `route_recommendation.yaml` | Next-step routing after pipeline exit | All families, all pipelines |
| `question_frame.yaml` | Bounded investigation scope | Inquiry/research, hypothesis_generation |
| `work_plan.yaml` | Ordered implementation slices | Forge/development, coding |
| `trust_assessment.yaml` | Trust assessment schema | Forensics/project_mapping |
| `provenance.yaml` | Artifact provenance schema | Forensics/project_mapping |

## Usage

Artifacts are validated against these schemas when added to state:

```python
from runtime.schemas.artifacts.validator import ArtifactValidator

validator = ArtifactValidator()
validator.validate("inventory_ledger", data)  # Raises if invalid
```
