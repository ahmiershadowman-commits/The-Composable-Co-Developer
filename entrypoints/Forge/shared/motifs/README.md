# Motifs

## Purpose

Motifs are semantic conditioning patterns that influence inference-time behavior. They act as lightweight, context-aware signals that guide the model's attention toward specific structural or semantic patterns without hardcoding rules.

## What Motifs Are

- **Inference-layer semantic conditioning**: Motifs shape how the model interprets context
- **Runtime weighting signals**: They adjust attention toward specific patterns
- **Hybrid interventions**: Part structural pattern, part semantic hint

## What Motifs Are NOT

- Not direct triggers (they don't invoke actions)
- Not hidden control logic (they don't bypass model autonomy)
- Not pipeline definitions (they don't define phase order)

## Motif Registry

Motifs are registered in `registry.yaml` with:
- Unique identifier
- Description of the pattern
- Detection signals
- Conditioning effect

## Available Motifs

| Motif | Purpose |
|-------|---------|
| `unfinished-proof` | Detects incomplete reasoning or evidence gaps |
| `watershed` | Marks decision points where direction matters |
| `tension_point` | Identifies conflicting claims or unresolved disputes |
| `absence_signal` | Surfaces missing information that should be present |

## Usage in Pipelines

Motifs are referenced in pipeline specs under `smallest_sufficient_interventions`:

```yaml
smallest_sufficient_interventions:
  motifs:
    - unfinished-proof
    - watershed
```

## Relationship to Other Layers

- **Primitives**: Motifs may suggest primitive invocation but don't trigger them
- **Operators**: Motifs can condition operator application
- **Evaluators**: Motifs may flag when evaluator scrutiny is warranted
- **Trace**: Trace may respond to motif signals with smallest-sufficient intervention

## Design Principle

Motifs preserve autonomy while improving pattern recognition. They scaffold the model toward more reliable behavior without becoming puppet-control strings.
