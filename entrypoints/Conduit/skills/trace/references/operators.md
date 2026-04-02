# Operators

Heavier local transformations that are still cheaper than a family reroute. Use operators when primitives have been tried and are insufficient.

## Operator registry

| Operator | When to use | Returns |
|---|---|---|
| `clarify` | A concept, claim, or output is ambiguous and the ambiguity is blocking progress | Disambiguated form with explicit scope |
| `compare` | Two or more options, claims, or artifacts need structured side-by-side evaluation | Comparison map with criteria and differential |
| `distill` | Accumulated material is too dense; key load-bearing content needs extraction | Compressed form preserving essential structure |
| `extract` | Specific content needs to be pulled from a larger artifact or context | Isolated extracted element with provenance note |
| `reframe` | The current problem formulation is not working; the question itself may be wrong | Reformulated problem statement or frame |
| `triangulate` | A claim or conclusion needs to be checked against multiple independent sources | Convergence/divergence map across sources |

## Invocation spectrum

The spectrum from least to most invasive:

```
primitive → operator → evaluator (via Lever) → pipeline pivot → cross-family reroute
```

Operators sit between primitives and evaluators. Use when:
- The primitive resolved the symptom but not the root problem
- Multiple passes of a primitive haven't converged
- A structured transformation (not just an attention adjustment) is needed
- A family reroute would be premature

## Usage rules

- Use the narrowest operator that addresses the specific problem
- `reframe` is expensive — exhaust other operators first
- `triangulate` requires at least 2-3 genuinely independent sources
- Do not use operators as evaluator substitutes when adjudication is explicitly needed
