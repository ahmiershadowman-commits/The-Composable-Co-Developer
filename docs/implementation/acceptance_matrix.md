# Acceptance Matrix

## Purpose

This matrix defines acceptance criteria for each family and pipeline. A pipeline is complete only when all its acceptance criteria are met.

## Acceptance Levels

| Level | Meaning |
|-------|---------|
| **Green** | All criteria met, ready for transition |
| **Yellow** | Minor gaps, acceptable with caveats |
| **Red** | Critical criteria missing, cannot transition |

---

## Forensics Family

### project_mapping

| Criterion | Required | Verification |
|-----------|----------|--------------|
| inventory_ledger present | Yes | File exists, non-empty |
| physical_dependency_graph present | Yes | Graph has nodes |
| discrepancy_ledger present | Yes | Even if empty |
| trust_zone_map present | Yes | Trust level assigned |
| canonical_source_note present | Yes | Sources identified |
| route_recommendation present | Yes | Valid target |
| trust_assessment updated | Yes | All fields populated |

**Exit gate**: All criteria must be Green

### defragmentation

| Criterion | Required | Verification |
|-----------|----------|--------------|
| fragmentation_snapshot present | Yes | Snapshot data exists |
| entropy_classification present | Yes | Severity assigned |
| chosen_method present | Yes | Method selected |
| residue_disposition_ledger present | Yes | Disposition recorded |
| metadata_normalization_record present | Yes | Normalization complete |
| trust_reassessment_note present | Yes | Coherence status set |
| route_recommendation present | Yes | Valid target |
| coherence_restored | Yes | Trust level improved |

**Exit gate**: coherence_restored must be true for Green

### documentation_audit

| Criterion | Required | Verification |
|-----------|----------|--------------|
| documentation_inventory present | Yes | Docs listed |
| code_state_inventory present | Yes | Code files listed |
| drift_ledger present | Yes | Even if empty |
| gap_analysis present | Yes | Gaps identified |
| audit_report present | Yes | Summary generated |
| route_recommendation present | Yes | Valid target |

**Exit gate**: All criteria must be present

### anomaly_disambiguation

| Criterion | Required | Verification |
|-----------|----------|--------------|
| anomaly_catalog present | Yes | Anomalies listed |
| anomaly_classification present | Yes | Types assigned |
| disambiguation_options present | Yes | Options generated |
| recommended_path present | Yes | Path selected |
| route_recommendation present | Yes | Valid target |

**Exit gate**: All criteria must be present

---

## Forge Family

### development

| Criterion | Required | Verification |
|-----------|----------|--------------|
| problem_frame present | Yes | Problem defined |
| architecture_note present | Yes | Approach documented |
| work_plan present | Yes | Slices defined |
| verification_summary present | Yes | Approach validated |
| route_recommendation present | Yes | Valid target |

**Exit gate**: work_plan must have at least one slice

### coding

| Criterion | Required | Verification |
|-----------|----------|--------------|
| change_plan present | Yes | Steps defined |
| changed_artifact present | Yes | Change made |
| validation_note present | Yes | Change validated |
| route_recommendation present | Yes | Valid target |

**Exit gate**: changed_artifact must exist

### testing

| Criterion | Required | Verification |
|-----------|----------|--------------|
| test_strategy present | Yes | Strategy defined |
| test_results present | Yes | Tests executed |
| test_report present | Yes | Summary generated |
| route_recommendation present | Yes | Valid target |

**Exit gate**: test_results must exist

### refactor

| Criterion | Required | Verification |
|-----------|----------|--------------|
| current_shape_map present | Yes | Shape documented |
| invariants_ledger present | Yes | Invariants listed |
| refactor_plan present | Yes | Plan defined |
| behavior_validation present | Yes | Behavior preserved |
| route_recommendation present | Yes | Valid target |

**Exit gate**: behavior_validation must confirm preservation

---

## Inquiry Family

### research

| Criterion | Required | Verification |
|-----------|----------|--------------|
| question_frame present | Yes | Question defined |
| source_ledger present | Yes | Sources listed |
| comparison_map present | Yes | Perspectives compared |
| synthesis_note present | Yes | Synthesis written |
| support_and_gap_map present | Yes | Gaps identified |
| route_recommendation present | Yes | Valid target |

**Exit gate**: synthesis_note must exist

### hypothesis_generation

| Criterion | Required | Verification |
|-----------|----------|--------------|
| candidate_set present | Yes | Candidates listed |
| discriminator_list present | Yes | Discriminators identified |
| provisional_selection present | Yes | Selection made |
| evidence_gap_note present | Yes | Gaps documented |
| route_recommendation present | Yes | Valid target |

**Exit gate**: candidate_set must have 2+ candidates

### formalization

| Criterion | Required | Verification |
|-----------|----------|--------------|
| concept_packet present | Yes | Concepts listed |
| object_relation_map present | Yes | Relations mapped |
| assumption_ledger present | Yes | Assumptions surfaced |
| definition_set present | Yes | Terms defined |
| notation_sheet present | Yes | Notation established |
| route_recommendation present | Yes | Valid target |

**Exit gate**: All criteria must be present

### mathematics

| Criterion | Required | Verification |
|-----------|----------|--------------|
| problem_statement present | Yes | Problem stated |
| assumptions_ledger present | Yes | Assumptions listed |
| derivation_record present | Yes | Derivation complete |
| edge_case_notes present | Yes | Edge cases checked |
| rigor_assessment present | Yes | Rigor evaluated |
| result_artifact present | Yes | Result stated |
| route_recommendation present | Yes | Valid target |

**Exit gate**: derivation_record must exist

---

## Conduit Family

### documentation

| Criterion | Required | Verification |
|-----------|----------|--------------|
| audience_scope_note present | Yes | Audience defined |
| source_packet present | Yes | Sources gathered |
| structure_outline present | Yes | Outline created |
| draft_document present | Yes | Draft written |
| support_note present | Yes | Claims verified |
| route_recommendation present | Yes | Valid target |

**Exit gate**: draft_document must exist

### handoff_synthesis

| Criterion | Required | Verification |
|-----------|----------|--------------|
| handoff_scope_note present | Yes | Scope defined |
| handoff_source_packet present | Yes | Sources gathered |
| core_structure_map present | Yes | Structure mapped |
| handoff_document present | Yes | Handoff written |
| unresolveds_and_risks present | Yes | Unresolveds listed |
| provenance_summary present | Yes | Provenance documented |
| next_safe_steps present | Yes | Next steps defined |

**Exit gate**: All criteria must be present

### professional_writing

| Criterion | Required | Verification |
|-----------|----------|--------------|
| audience_objective_statement present | Yes | Objective defined |
| outline present | Yes | Outline created |
| draft_document present | Yes | Draft written |
| refinement_log present | Yes | Refinements recorded |
| validation_note present | Yes | Validated |
| delivery_record present | Yes | Delivered |

**Exit gate**: delivery_record must exist

### scholarly_writing

| Criterion | Required | Verification |
|-----------|----------|--------------|
| genre_frame present | Yes | Genre defined |
| source_packet present | Yes | Sources gathered |
| outline present | Yes | Outline created |
| claim_hierarchy present | Yes | Claims mapped |
| draft present | Yes | Draft written |
| citation_map present | Yes | Citations mapped |
| final_document present | Yes | Finalized |

**Exit gate**: final_document must exist

---

## Verification Process

### Automated Checks

```python
def verify_acceptance(pipeline_id, state):
    criteria = ACCEPTANCE_MATRIX[pipeline_id]
    results = {}
    
    for criterion in criteria:
        artifact_name = criterion['artifact']
        required = criterion['required']
        
        if artifact_name in state.artifacts:
            results[criterion['name']] = "GREEN"
        elif required:
            results[criterion['name']] = "RED"
        else:
            results[criterion['name']] = "YELLOW"
    
    return results
```

### Manual Review

Some criteria require human judgment:
- Quality of synthesis
- Completeness of derivation
- Adequacy of test coverage

## Escalation Rules

| Pattern | Action |
|---------|--------|
| All Green | Proceed to next pipeline |
| Any Red | Cannot exit pipeline |
| Multiple Yellow | Consider additional work |
| Critical criterion Yellow | Escalate to Trace |
