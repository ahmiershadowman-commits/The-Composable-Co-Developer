# Inquiry Artifact Contracts

After running any Inquiry pipeline, read artifacts from `runtime_output/Inquiry/<pipeline_id>/`.

## research

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `question_frame` | Bounded statement of what is being investigated |
| `source_ledger` | Sources consulted with trust classification |
| `comparison_map` | Structured side-by-side of competing evidence or options |
| `synthesis_note` | What the evidence converges on |
| `support_and_gap_map` | Where support is sufficient and where gaps remain |
| `route_recommendation` | Next step (often pipeline:Inquiry/hypothesis_generation if explanation is open) |

## hypothesis_generation

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `phenomenon_description` | The observation or anomaly being explained |
| `candidate_set` | Generated explanatory hypotheses |
| `discriminator_list` | What evidence would distinguish between candidates |
| `provisional_selection_note` | Which hypothesis is best supported currently |
| `evidence_gap_note` | What evidence is needed to confirm or eliminate |
| `route_recommendation` | Next step (back to research if evidence gap is large) |

## formalization

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `concept_packet` | Concepts identified and scoped |
| `object_relation_map` | Explicit relations between concepts |
| `assumption_ledger` | Assumptions being made and their load-bearing status |
| `definition_set` | Formal definitions |
| `notation_sheet` | Notation used |
| `route_recommendation` | Next step (often pipeline:Inquiry/mathematics when stable) |

## mathematics

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `problem_statement` | Formal statement of what is being proved or derived |
| `assumptions_ledger` | Explicit assumptions with justification |
| `derivation_record` | Step-by-step derivation or proof |
| `edge_case_notes` | Boundary conditions and their handling |
| `rigor_assessment` | Self-assessment of proof completeness |
| `result_artifact` | The result (theorem, derivation, counterexample) |
| `route_recommendation` | Next step |

## Inquiry→Forensics trigger

If any of the following appear mid-investigation, stop and reroute to Forensics:
- `source_truth_suspect` — sources cannot be trusted
- `anomaly_source_ambiguous` — the anomaly itself has unclear origin
- `documentation_or_state_claims_untrusted` — what is being investigated rests on an untrusted surface
