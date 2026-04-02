# Trace Recurring Microcheck

Apply after each bounded step in any active pipeline.

| Check | Question | On fail |
|---|---|---|
| `right_phase` | Are we still in the right phase? | pivot_or_escalate |
| `legal_next_move` | Is the current next move legal under the active pipeline and policy? | stop_and_reselect |
| `method_pivot_trigger` | Has a local pivot condition fired? | pivot_within_pipeline |
| `artifact_drift` | Has the artifact drifted enough to require cleanup, normalization, or reevaluation? | invoke_cleanup_or_defragmentation_method |
| `metadata_drift` | Has metadata or provenance changed enough to require tidying or re-indexing? | normalize_metadata |
| `contradiction_pressure` | Is contradiction or tension now high enough that local handling may be insufficient? | consider_lever |
| `confidence_support_gap` | Is local confidence rising faster than evidence quality? | invoke_evaluator_or_reweight |
| `branch_sprawl` | Have too many live branches accumulated without synthesis or discrimination? | synthesis_or_discrimination |
| `trust_collapse` | Has trust in the visible surface collapsed enough to justify a Forensics reset? | reset_to_forensics |
| `smallest_sufficient_intervention` | Can this be handled with a smaller intervention than rerouting? | escalate_one_level_only |

## Rubric domains (deeper evaluation when needed)

**phase_fit**: Is the active phase still correct? Has a phase transition become justified? Is the current phase being overextended?

**method_fit**: Is the current local method still appropriate? Has a method-specific pivot trigger fired? Is a smaller intervention sufficient?

**artifact_state**: Has artifact shape drifted from the pipeline's target form? Has metadata changed enough to require normalization? Has residue accumulated that should be preserved, cleaned, or indexed?

**epistemic_state**: Is confidence outrunning support? Is contradiction present, unresolved, or merely apparent? Is the active frame suspiciously comfortable or under-discriminated?

**routing_state**: Is a motif nudge enough? Is a primitive enough? Is a local evaluator justified? Has trust dropped enough to require Forensics?

## Selection bias

Default rule: smallest_sufficient_intervention
Escalation boundary: local_evaluator
Preserve residue by default: true
