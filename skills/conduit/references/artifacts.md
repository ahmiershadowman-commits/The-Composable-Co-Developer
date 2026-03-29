# Conduit Artifact Contracts

After running any Conduit pipeline, read artifacts from `runtime_output/Conduit/<pipeline_id>/`.

## documentation

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `audience_scope_note` | Who the documentation is for and what scope it covers |
| `source_packet` | Source material used |
| `structure_outline` | Proposed structure before drafting |
| `draft_document` | The written documentation |
| `support_note` | Assessment of whether all claims are supported |
| `metadata_update_record` | What metadata was created or updated |
| `route_recommendation` | Next step (Conduit/handoff_synthesis if compression needed) |

**Check `support_note` before delivering** — if unsupported claims are flagged, route to Inquiry first.

## handoff_synthesis

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `handoff_scope_note` | What is being handed off and to whom |
| `handoff_source_packet` | Source material to be synthesized |
| `core_structure_map` | Load-bearing structure identified (must not be compressed away) |
| `handoff_document` | The synthesized handoff artifact |
| `unresolveds_and_risks` | Open issues and risks that must transfer with the handoff |
| `provenance_summary` | Where the synthesized content came from |
| `next_safe_steps` | What the receiver should do first |

**Critical**: `unresolveds_and_risks` must be present. Do not compress away load-bearing structure.

## scholarly_writing

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `genre_frame` | What kind of scholarly document this is and its conventions |
| `source_packet` | Sources with trust and relevance assessment |
| `outline` | Structural outline of the argument |
| `claim_hierarchy` | Main claim → supporting claims → evidence |
| `draft` | The written document |
| `citation_map` | Claims mapped to supporting citations |
| `final_document` | Final output |

If `claim_hierarchy` reveals weak support → route to Inquiry before drafting.

## professional_writing

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `audience_objective_statement` | Who is reading this and what decision or action it supports |
| `outline` | Structural outline |
| `draft_document` | The written professional document |
| `refinement_log` | Revisions made and why |
| `validation_note` | Whether the document achieves its stated objective |
| `delivery_record` | Format and delivery destination |

## Conduit→Forensics trigger

If any of the following appear during writing, stop and reroute:
- `documentation_truth_unclear` — what is being documented cannot be trusted
- `source_material_conflicts_with_observed_state` — sources disagree with reality

## Anti-pattern: rendering unsupported claims

Conduit must not render unsupported claims without rerouting to Inquiry. Check `support_note` or `claim_hierarchy` for flags before delivering any Conduit output.
