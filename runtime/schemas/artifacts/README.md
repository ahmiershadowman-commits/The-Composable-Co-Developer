# Artifact Schemas

Schema definitions for all runtime artifacts.

## Available Schemas

| Schema | Description |
|--------|-------------|
| `inventory_ledger.yaml` | Project inventory schema |
| `route_decision.yaml` | Route decision schema |
| `trust_assessment.yaml` | Trust assessment schema |
| `provenance.yaml` | Artifact provenance schema |

## Usage

Artifacts are validated against these schemas when added to state:

```python
from runtime.schemas.artifacts.validator import ArtifactValidator

validator = ArtifactValidator()
validator.validate("inventory_ledger", data)  # Raises if invalid
```
