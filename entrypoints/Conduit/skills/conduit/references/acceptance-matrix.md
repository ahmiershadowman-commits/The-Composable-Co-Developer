# Conduit — Acceptance Matrix

Exit criteria that must be satisfied before declaring a Conduit pipeline complete.

## documentation (Clarify)

| Criterion | Check | Required |
|-----------|-------|----------|
| Audience and purpose stated | Who is reading this and what decision it supports | Yes |
| Draft produced | `draft_document.yaml` or `.md` present | Yes |
| Claims supported | `support_note.yaml` — no unsupported claims in draft | Yes |
| Unresolveds surfaced | `unresolveds_and_risks.yaml` present | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: Audience not stated; unsupported claims silently included; unresolveds not surfaced.

---

## handoff_synthesis (Distill)

| Criterion | Check | Required |
|-----------|-------|----------|
| Source material analyzed | Accumulated content identified before compression | Yes |
| Load-bearing structure preserved | `handoff_document.yaml` — no essential structure compressed away | Yes |
| Claim hierarchy documented | `claim_hierarchy.yaml` present | Yes |
| Unresolveds transferred | `unresolveds_and_risks.yaml` must accompany any handoff | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: Handoff without `unresolveds_and_risks`; load-bearing structure compressed; source material not analyzed before synthesis.

---

## scholarly_writing (Articulate)

| Criterion | Check | Required |
|-----------|-------|----------|
| Argument stated | Thesis or claim is explicit | Yes |
| Evidence cited | All claims have supporting sources | Yes |
| Counterarguments addressed | Opposing views engaged | Yes |
| Formal output produced | `final_document.yaml` or `.md` present | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: Claims without evidence; counterarguments ignored; used for operational docs (wrong pipeline — use `documentation`).

---

## professional_writing (Convey)

| Criterion | Check | Required |
|-----------|-------|----------|
| Audience and context stated | Who is reading and what action is expected | Yes |
| Draft produced | `draft_document.yaml` present | Yes |
| Narrative coherent | Document has clear through-line | Yes |
| Claims supported | `support_note.yaml` — weak claims flagged | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

---

## Universal exit conditions (all pipelines)

1. Output audience and purpose are explicit — stated in the document or `scope_note`
2. Load-bearing structure from source material is preserved (not compressed away)
3. Unsupported claims are flagged in `support_note`, not silently included
4. `unresolveds_and_risks.yaml` present — mandatory for any handoff
5. All required artifacts written to `runtime_output/Conduit/<pipeline_id>/`
6. If documentation truth becomes unclear mid-render: stop, reroute to Forensics
