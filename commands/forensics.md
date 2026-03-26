# /forensics

**Ground-truth establishment for ambiguous or fragmented project states.**

Use this command when you need to understand a project's actual state before making changes, especially when documentation is suspect, the codebase is fragmented, or there are conflicting signals about how things work.

## Usage

```
/forensics [pipeline] [scope]
```

## Pipelines

| Pipeline | When to use |
|----------|-------------|
| `project_mapping` | Map the current project state, identify trust zones, and get routing recommendations |
| `defragmentation` | Restore coherence when project structure has become fragmented or drifted |
| `documentation_audit` | Verify documentation accuracy against actual code |
| `anomaly_disambiguation` | Investigate conflicting signals or anomalous behavior |

## Examples

```
/forensics project_mapping Map the authentication module before refactoring
/forensics defragmentation The docs and code have diverged significantly
/forensics documentation_audit Check if the API docs match the implementation
/forensics anomaly_disambiguation Tests pass but production is failing
```

## Output

Artifacts are written to `runtime_output/` and include:
- `inventory_ledger.yaml` - Complete project inventory
- `physical_dependency_graph.yaml` - Actual dependency structure
- `discrepancy_ledger.yaml` - Identified conflicts
- `trust_zone_map.yaml` - Trust assessment by area
- `route_recommendation.yaml` - Recommended next steps

## Related Commands

- `/forge` - After Forensics establishes ground truth, use Forge to build
- `/inquiry` - For investigation when ground truth is already established
- `/conduit` - For documentation once state is understood
