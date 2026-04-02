---
name: trace
description: >
  This skill should be used when actively working inside any pipeline (Forensics, Forge, Inquiry,
  or Conduit) and supervision is needed — when deciding what intervention to apply next, when
  something feels off mid-pipeline, when a pivot condition may have fired, or when escalation
  to Lever or Residue is being considered. Also triggers on "what should I do next here",
  "should I escalate this", "the current approach isn't working", "there's a contradiction I
  haven't resolved", "confidence is outrunning evidence", "too many branches", or any situation
  where the smallest-sufficient intervention needs to be selected before continuing.
metadata:
  version: "0.1.0"
  authority: Trace
---

# Trace — Metacognitive Supervisor

Trace is the traveling metacognitive controller. It runs throughout all pipeline work — not as a separate step the user invokes, but as continuous supervision of what intervention is needed next. When working in any family pipeline, apply Trace supervision before escalating or rerouting.

## Core principle: smallest-sufficient intervention

Always select the smallest intervention that resolves the current problem before escalating. The intervention order, from least to most invasive:

```
motif → primitive → selector_self_check → local_evaluator →
phase_pivot → sibling_pipeline_shift → heavy_skill →
cross_family_reroute → forensic_reset
```

Do not skip levels. Reach for reroute only after the cheaper options have been considered and found insufficient.

## When to apply Trace supervision

Apply a Trace check after each bounded step. The recurring microcheck questions:

1. Are we still in the right phase?
2. Is the current next move legal under the active pipeline?
3. Has a local pivot condition fired?
4. Has the artifact drifted enough to require cleanup or re-evaluation?
5. Has metadata or provenance changed enough to require normalization?
6. Is contradiction or tension high enough that local handling may be insufficient?
7. Is local confidence rising faster than evidence quality?
8. Have too many live branches accumulated without discrimination?
9. Has trust collapsed enough to justify a Forensics reset?
10. Can this be handled with a smaller intervention than rerouting?

See `references/checklist.md` for the full structured form.

## Authority routing

### Trace handles directly
- Routine micro-checks
- Smallest-sufficient intervention selection (motif, primitive, operator)
- Ordinary routing supervision
- Phase pivots and sibling pipeline shifts

### Escalate to Residue when
- A suspicious surface signal appears (misfit, absence, tension, warp, offset)
- Something feels smoothed, incomplete, or structurally odd without a clear explanation
- Lens-based interpretation is needed before a route decision can be made

Residue applies a lens and returns an interpretation. Trace then incorporates it into the route decision. Residue does NOT make commitment decisions.

### Escalate to Lever when
- Trace's smallest-sufficient handling is inadequate
- Explicit evaluator adjudication is required (contradiction, support gap, frame error, discriminator, shape drift)
- A commitment or reopen decision is needed

**Forbidden order**: Lever must never be invoked before Trace has attempted handling.

## Trigger-to-authority quick reference

| Trigger | First response |
|---|---|
| `phase_mismatch` | Phase pivot (Trace) |
| `confidence_support_mismatch` | Primitive → support_evaluator if insufficient (Lever) |
| `branch_sprawl` | Primitive `trim` → discriminator_evaluator (Lever) |
| `trust_collapse` | Cross-family reroute to Forensics |
| `artifact_shape_drift` | Local cleanup → defragmentation if structural |
| `misfit_detected` | Residue `misfit` lens |
| `absence_detected` | Residue `absence` lens |
| `tension_detected` | Residue `tension` lens → Lever if adjudication needed |
| `contradiction_requires_adjudication` | Lever contradiction_evaluator |
| `discriminator_required` | Lever discriminator_evaluator |

## References

- `references/checklist.md` — Full Trace microcheck checklist
- `references/primitives.md` — 12 primitives (metacognitive + reasoning)
- `references/operators.md` — 6 operators
- `references/motifs.md` — 4 core motifs
- `references/residue-lenses.md` — 8 Residue lenses with trigger conditions
- `references/lever-evaluators.md` — 6 Lever evaluators with use conditions
