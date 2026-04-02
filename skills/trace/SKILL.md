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

- `references/checklist.md` — Read this when running a structured Trace microcheck; contains the full 10-question form with decision branches.
- `references/primitives.md` — Read this when selecting a primitive intervention; contains all 12 primitives with use conditions.
- `references/operators.md` — Read this when selecting an operator; contains all 6 operators with trigger conditions.
- `references/motifs.md` — Read this when a motif-level intervention may be sufficient; contains the 4 core motifs.
- `references/residue-lenses.md` — Read this when a suspicious surface signal appears and lens-based interpretation is needed before a route decision.
- `references/lever-evaluators.md` — Read this when escalating to Lever; contains all 6 evaluators with use conditions and adjudication criteria.

## Anti-patterns

**Do not skip the intervention ladder and jump directly to reroute.** Every level skipped is cost added — cross-family reroutes and forensic resets are expensive. A primitive or motif resolves most problems. Reach for reroute only after cheaper options are exhausted.

**Do not invoke Lever before Trace has attempted handling.** Lever is for adjudication when Trace is genuinely insufficient — not for the first sign of difficulty. Premature Lever invocation inflates authority overhead and trains the wrong escalation reflex.

**Do not treat a microcheck as optional when confidence is rising.** Confidence that outruns evidence is the most common failure mode in pipeline work. Skipping the check because things feel like they're going well is exactly when the check matters most.

**Do not route to Residue for decisions Trace can handle directly.** Residue applies lenses and returns interpretations — it does not make commitment decisions. Routing to Residue for something that is already resolvable by a primitive or phase pivot adds interpretation overhead without adding clarity.
