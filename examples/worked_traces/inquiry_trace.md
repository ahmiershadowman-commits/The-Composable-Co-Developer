# Inquiry Trace

## Purpose

This worked trace demonstrates the full Inquiry family execution flow, from research question through formalization.

## Trace Overview

**Route**: Forensics → Inquiry → Conduit

**Pipelines executed**:
1. Forensics/project_mapping (ground truth)
2. Inquiry/research (investigation)
3. Inquiry/hypothesis_generation (explanation building)
4. Inquiry/formalization (structure definition)
5. Conduit/documentation (communication)

---

## Step 1: Forensics/project_mapping

**Entry condition**: New project, state unknown

**Context**:
```yaml
scope:
  description: "Research project state mapping"
  boundaries: ["src/", "docs/", "tests/"]
artifacts:
  - src/main.py
  - src/utils.py
  - docs/README.md
  - tests/test_main.py
```

**Artifacts produced**:
- `inventory_ledger` - 4 files inventoried
- `physical_dependency_graph` - main.py → utils.py
- `discrepancy_ledger` - 1 discrepancy (docs reference missing module)
- `trust_zone_map` - trust_level: medium
- `canonical_source_note` - observed_filesystem is canonical
- `route_recommendation` - target: family:Inquiry

**Trust assessment**:
```yaml
trust_level: medium
canonical_sources_identified: true
discrepancy_count: 1
requires_forensics: false
requires_defragmentation: false
```

---

## Step 2: Inquiry/research

**Entry condition**: Trust established, research question identified

**Context**:
```yaml
question: "What is the optimal architecture for this system?"
scope: "broad"
```

**Phases executed**:
1. frame_question → `question_frame`
2. gather_sources → `source_ledger` (3 sources)
3. compare_perspectives → `comparison_map` (2 perspectives)
4. synthesize → `synthesis_note`
5. map_support_gaps → `support_and_gap_map` (2 gaps identified)
6. recommend_route → `route_recommendation`

**Route decision**: Continue to hypothesis_generation (gaps need explanation)

---

## Step 3: Inquiry/hypothesis_generation

**Entry condition**: Research identified gaps needing explanation

**Context**:
```yaml
phenomenon: "System has performance issues"
observations:
  - "High latency on startup"
  - "Memory usage grows over time"
```

**Phases executed**:
1. understand_phenomenon → `phenomenon_description`
2. generate_candidates → `candidate_set` (3 candidates)
3. identify_discriminators → `discriminator_list` (2 discriminators)
4. provisional_selection → `provisional_selection_note`
5. map_evidence_gaps → `evidence_gap_note`
6. recommend_route → `route_recommendation`

**Route decision**: Continue to formalization (hypothesis selected)

---

## Step 4: Inquiry/formalization

**Entry condition**: Hypothesis selected, needs formal structure

**Context**:
```yaml
concepts:
  - "lazy_initialization"
  - "connection_pooling"
  - "cache_invalidation"
```

**Phases executed**:
1. identify_concepts → `concept_packet`
2. map_relations → `object_relation_map`
3. surface_assumptions → `assumption_ledger`
4. define_terms → `definition_set`
5. establish_notation → `notation_sheet`
6. recommend_route → `route_recommendation`

**Route decision**: Ready for Conduit (formalization complete)

---

## Step 5: Conduit/documentation

**Entry condition**: Formal structure ready for communication

**Context**:
```yaml
audience: "technical_team"
scope: "architecture_documentation"
```

**Phases executed**:
1. scope_audience → `audience_scope_note`
2. gather_sources → `source_packet`
3. outline_structure → `structure_outline`
4. draft → `draft_document`
5. verify_support → `support_note`
6. update_metadata → `metadata_update_record`
7. recommend_route → `route_recommendation`

**Route decision**: Documentation complete

---

## Route History

| Step | Pipeline | Trust | Route Decision |
|------|----------|-------|----------------|
| 1 | Forensics/project_mapping | medium | → Inquiry |
| 2 | Inquiry/research | medium | → hypothesis_generation |
| 3 | Inquiry/hypothesis_generation | medium | → formalization |
| 4 | Inquiry/formalization | medium | → Conduit |
| 5 | Conduit/documentation | high | → complete |

---

## Key Learnings

1. **Trust preserved**: No trust collapse during Inquiry work
2. **Progressive refinement**: Each pipeline added structure
3. **Clean transitions**: All route recommendations valid
4. **Artifact accumulation**: 20+ artifacts produced

---

## Validation Checklist

- [x] All pipelines executed in legal order
- [x] All artifacts produced match pipeline specs
- [x] All route decisions resolve to valid targets
- [x] Trust assessment updated appropriately
- [x] No forbidden transitions occurred

---

## Trace File

Location: `examples/worked_traces/inquiry_trace.md`

Test: `tests/worked_examples/test_inquiry_trace.py`
