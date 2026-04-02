# Lever Evaluators

Lever is the evaluator / escalation / commitment authority. It is invoked only after Trace has attempted smallest-sufficient handling and found it inadequate. Lever makes adjudication decisions, handles escalation, and owns commitment and reopen calls.

**Forbidden**: Never invoke Lever before Trace has evaluated. Lever does not substitute for Residue lens interpretation. Lever does not act independently — it is always reached through Trace escalation.

## Evaluator registry

### contradiction_evaluator
**Use when**: Contradiction detected AND local primitives failed to resolve conflict
**Returns**: contradiction_classification, materiality_assessment, local_resolution_or_reroute_recommendation

### discriminator_evaluator
**Use when**: Branch sprawl without clear discriminators; multiple candidates compete without evidence ranking
**Returns**: discriminator_set, candidate_ranking_basis, synthesis_or_pruning_recommendation

### support_evaluator
**Use when**: Confidence-support gap is present; claim consequence class is high
**Returns**: support_sufficiency_assessment, downgrade_hold_or_research_recommendation

### frame_evaluator
**Use when**: Wrong-question risk is present; repeated local failure with stable surface; route choice may be masking a frame error
**Returns**: frame_fit_assessment, reframe_or_recenter_recommendation

### trust_evaluator
**Use when**: Suspect documentation; canonical conflict; provenance uncertainty
**Returns**: trust_zone_map, forensics_required_boolean, temporary_safe_scope_if_any

### artifact_shape_evaluator
**Use when**: Structure drift; metadata incoherence; handoff risk due to artifact sprawl
**Returns**: shape_violation_list, cleanup_or_defragmentation_recommendation

## Response contract

Every Lever evaluator response must return:
- `recommended_action` — what to do next
- `rationale` — why
- `intervention_level` — how invasive the recommended action is
- `residue_to_preserve` — what not to discard
- `target` — the canonical target grammar address of the next step

May also return: `evaluator_notes`, `confidence_calibration`

## Escalation order

```
Trace evaluates
  → Trace determines insufficiency
    → Escalate to Lever
      → Lever selects evaluator
        → Evaluator produces judgment
          → Lever makes commitment/reopen decision
```

Lever only makes a commitment decision after evaluator judgment. It does not commit preemptively.
