# Conduit Fallback Trace

## Purpose

This worked trace demonstrates recovery from trust collapse through Forensics to Conduit for documentation reconciliation.

## Trace Overview

**Route**: Trust Collapse → Forensics/defragmentation → Conduit/handoff_synthesis

**Scenario**: Documentation has drifted from actual implementation, causing confusion and failed handoffs.

---

## Step 1: Trust Collapse Detected

**Trigger**: Conduit/documentation attempts to render but support verification fails

**Symptoms**:
- Claims in docs don't match code behavior
- Multiple conflicting documentation versions
- Stakeholders report confusion

**Trust assessment**:
```yaml
trust_level: collapsed
canonical_sources_identified: false
discrepancy_count: 5
entropy_level: high
requires_forensics: true
```

**Route decision**: forensics_reset

---

## Step 2: Forensics/defragmentation

**Entry condition**: Trust collapsed, entropy primary

**Context**:
```yaml
artifacts:
  - docs/architecture_v1.md
  - docs/architecture_v2.md
  - docs/api_reference.md
  - src/api.py
  - src/core.py
metadata_issues:
  - "Conflicting version numbers"
  - "Missing last_updated fields"
structural_issues:
  - "Docs reference removed modules"
```

**Phases executed**:
1. inspect_state → `fragmentation_snapshot`
   - 5 duplicate artifacts
   - 3 naming drift issues
   - 2 structural conflicts

2. classify_entropy → `entropy_classification`
   - severity: repair
   - issue_count: 5

3. choose_method → `chosen_method`
   - method: repair
   - rationale: "Project shape has drifted"

4. execute_method → `residue_disposition_ledger`, `changed_structure_map`
   - 3 artifacts merged
   - 2 artifacts archived

5. normalize_metadata → `metadata_normalization_record`
   - canonical_pointers_updated: true
   - indices_rebuilt: true

6. verify_coherence → `trust_reassessment_note`
   - coherence_status: restored
   - confidence: high

7. finalize_reroute → `route_recommendation`
   - target: family:Conduit
   - reason: "docs_handoff_reconciliation_needed"

**Trust assessment after**:
```yaml
trust_level: medium
canonical_sources_identified: true
discrepancy_count: 0
entropy_level: low
coherence_restored: true
```

---

## Step 3: Conduit/handoff_synthesis

**Entry condition**: Coherence restored, handoff needed

**Context**:
```yaml
recipient: "new_team_member"
purpose: "knowledge_transfer"
```

**Phases executed**:
1. scope_handoff → `handoff_scope_note`
2. gather_sources → `handoff_source_packet`
3. map_core_structure → `core_structure_map`
4. synthesize_handoff → `handoff_document`
5. note_unresolveds → `unresolveds_and_risks`
6. summarize_provenance → `provenance_summary`
7. recommend_next_steps → `next_safe_steps`

**Artifacts produced**:
- `handoff_scope_note` - recipient: new_team_member
- `handoff_source_packet` - 5 sources
- `core_structure_map` - architecture overview
- `handoff_document` - complete handoff
- `unresolveds_and_risks` - 2 open items
- `provenance_summary` - full route history
- `next_safe_steps` - onboarding checklist

---

## Route History

| Step | Pipeline | Trust Before | Trust After | Route Decision |
|------|----------|--------------|-------------|----------------|
| 1 | Trust collapse | high | collapsed | → forensics_reset |
| 2 | Forensics/defragmentation | collapsed | medium | → Conduit |
| 3 | Conduit/handoff_synthesis | medium | high | → complete |

---

## Key Learnings

1. **Trust collapse handled correctly**: Immediate forensics_reset
2. **Defragmentation restored coherence**: entropy → order
3. **Conduit reconciliation successful**: handoff produced
4. **Provenance preserved**: Full route history documented

---

## Validation Checklist

- [x] Trust collapse triggered forensics_reset
- [x] Defragmentation selected appropriate method (repair)
- [x] Coherence verified before Conduit entry
- [x] Handoff includes unresolveds and provenance
- [x] No forbidden transitions occurred

---

## Trace File

Location: `examples/worked_traces/conduit_fallback_trace.md`

Test: `tests/worked_examples/test_conduit_fallback_trace.py`
