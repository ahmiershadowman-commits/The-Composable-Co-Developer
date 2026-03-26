# Trust Assessment Schema

## Purpose

Records the trust level and canonical source status determined during Forensics analysis.

## Schema

```yaml
trust_assessment:
  type: object
  required: true
  description: Assessment of state trustworthiness
  properties:
    trust_level:
      type: string
      required: true
      enum: [high, medium, low, collapsed]
      description: Overall trust level
    canonical_sources_identified:
      type: boolean
      required: true
      description: Whether canonical sources are identified
    discrepancy_count:
      type: number
      required: true
      description: Number of discrepancies found
    entropy_level:
      type: string
      enum: [high, low]
      description: Level of fragmentation/entropy
    coherence_restored:
      type: boolean
      description: Whether defragmentation restored coherence
    requires_forensics:
      type: boolean
      required: true
      description: Whether Forensics intervention needed
    requires_defragmentation:
      type: boolean
      required: true
      description: Whether defragmentation needed
```

## Example

```yaml
trust_level: high
canonical_sources_identified: true
discrepancy_count: 0
entropy_level: low
coherence_restored: true
requires_forensics: false
requires_defragmentation: false
```

## Trust Level Definitions

| Level | Meaning | Downstream Allowed |
|-------|---------|-------------------|
| high | Canonical sources identified, no discrepancies | Forge, Inquiry, Conduit |
| medium | Minor discrepancies, canonical unclear | Inquiry, Conduit |
| low | Significant discrepancies | Forensics only |
| collapsed | Trust completely failed | Forensics reset required |

## Usage

Produced by: All Forensics pipelines

Consumed by:
- `TraceSelector` for route decisions
- `TransitionEngine` for transition validation
- `LeverEscalation` for evaluator selection
