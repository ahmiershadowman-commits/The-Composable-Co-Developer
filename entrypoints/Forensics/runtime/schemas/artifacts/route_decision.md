# Route Decision Schema

## Purpose

Records routing decisions made by Trace selector during execution.

## Schema

```yaml
route_decision:
  type: object
  required: true
  description: Decision about next routing target
  properties:
    action:
      type: string
      required: true
      enum:
        - ROUTE
        - CROSS_FAMILY_REROUTE
        - PHASE_PIVOT
        - PIPELINE_SWITCH
        - FORENSICS_RESET
      description: Type of routing action
    target:
      type: string
      required: true
      description: Target identifier (canonical grammar)
    intervention_band:
      type: string
      enum:
        - LOCAL
        - PHASE
        - PIPELINE
        - CROSS_FAMILY_REROUTE
      description: Intervention scope
    reason:
      type: string
      required: true
      description: Rationale for decision
    family:
      type: string
      enum: [FORENSICS, FORGE, INQUIRY, CONDUIT]
      description: Target family (for cross-family)
    confidence:
      type: string
      enum: [high, medium, low]
      description: Confidence in decision
    timestamp:
      type: string
      format: date-time
      description: Decision timestamp
```

## Example

```yaml
action: CROSS_FAMILY_REROUTE
target: "family:Forge"
intervention_band: CROSS_FAMILY_REROUTE
reason: "State grounded - build work can proceed"
family: FORGE
confidence: high
timestamp: "2026-03-25T10:35:00Z"
```

## Canonical Target Grammar

Targets must follow canonical grammar:

| Pattern | Example |
|---------|---------|
| `pipeline:<Family>/<id>` | `pipeline:Forensics/project_mapping` |
| `family:<Family>` | `family:Forge` |
| `authority:<Authority>` | `authority:Trace` |
| `primitive:<name>` | `primitive:locate` |
| `operator:<name>` | `operator:distill` |
| `evaluator:<name>` | `evaluator:support_evaluator` |
| `forensics_reset` | `forensics_reset` |

## Usage

Produced by: `TraceSelector.evaluate()`

Consumed by:
- `TransitionEngine` for execution
- `ArtifactWriter` for provenance
- `RuntimeDispatcher` for next pipeline
