# Refactor vs Defragmentation Trace

## Purpose

This worked trace demonstrates the decision boundary between Forge/refactor and Forensics/defragmentation.

## Trace Overview

**Two scenarios compared**:
1. Local code smell → Forge/refactor (appropriate)
2. Project-wide drift → Forensics/defragmentation (appropriate)

---

## Scenario A: Forge/refactor (Local Issue)

### Entry Condition

**State**:
```yaml
trust_level: high
canonical_sources_identified: true
scope: "Single module"
```

**Problem**: Complex function needs simplification

**Context**:
```yaml
target_file: src/processing.py
function: process_data_complex()
issues:
  - "Function is 200+ lines"
  - "Multiple responsibilities"
  - "Hard to test"
```

### Pipeline Selection

**Trace evaluates**:
- Trust: high (no forensics needed)
- Scope: local (single function)
- Problem type: code structure

**Route decision**:
```yaml
target: pipeline:Forge/refactor
reason: "local_structure_improvement"
confidence: high
```

### Forge/refactor Execution

**Phases**:
1. map_current_shape → `current_shape_map`
2. identify_invariants → `invariants_ledger`
3. plan_refactor → `refactor_plan`
4. execute_refactor → `refactored_artifact`
5. validate_behavior → `behavior_validation`
6. recommend_next → `route_recommendation`

**Artifacts produced**:
- `current_shape_map` - before state
- `invariants_ledger` - public API, behavior
- `refactor_plan` - extract method steps
- `refactored_artifact` - simplified function
- `behavior_validation` - tests pass

**Route recommendation**:
```yaml
target: pipeline:Forge/testing
reason: "validation_needed"
```

### Why Refactor Was Correct

| Factor | Value | Appropriate for Refactor? |
|--------|-------|---------------------------|
| Trust level | high | ✅ Yes |
| Scope | single function | ✅ Yes |
| Canonical clarity | clear | ✅ Yes |
| Entropy | low (local only) | ✅ Yes |

---

## Scenario B: Forensics/defragmentation (Project-Wide Issue)

### Entry Condition

**State**:
```yaml
trust_level: low
canonical_sources_identified: false
scope: "Entire project"
```

**Problem**: Multiple conflicting architectures

**Context**:
```yaml
artifacts:
  - docs/architecture_monolith.md
  - docs/architecture_microservices.md
  - src/monolith/
  - src/services/
  - README.md (references both)
issues:
  - "Two architecture docs contradict"
  - "Code split between both approaches"
  - "Team confused about direction"
```

### Pipeline Selection

**Trace evaluates**:
- Trust: low (canonical unclear)
- Scope: project-wide
- Problem type: entropy/fragmentation

**Route decision**:
```yaml
target: pipeline:Forensics/defragmentation
reason: "entropy_primary"
confidence: high
```

### Forensics/defragmentation Execution

**Phases**:
1. inspect_state → `fragmentation_snapshot`
2. classify_entropy → `entropy_classification`
3. choose_method → `chosen_method`
4. execute_method → `residue_disposition_ledger`
5. normalize_metadata → `metadata_normalization_record`
6. verify_coherence → `trust_reassessment_note`
7. finalize_reroute → `route_recommendation`

**Key artifacts**:
- `fragmentation_snapshot` - 2 architectures, 5 conflicts
- `entropy_classification` - severity: anchor
- `chosen_method` - method: anchor (rollback needed)
- `residue_disposition_ledger` - 1 archived, 1 canonical
- `trust_reassessment_note` - coherence_restored: true

**Route recommendation**:
```yaml
target: pipeline:Forensics/project_mapping
reason: "recheck_needed_after_coherence"
```

### Why Defragmentation Was Correct

| Factor | Value | Appropriate for Defragmentation? |
|--------|-------|----------------------------------|
| Trust level | low | ✅ Yes |
| Scope | project-wide | ✅ Yes |
| Canonical clarity | conflicted | ✅ Yes |
| Entropy | high (multiple sources) | ✅ Yes |

---

## Decision Boundary

### Use Forge/refactor When

- ✅ Trust is high
- ✅ Canonical source is clear
- ✅ Problem is local (single file/module)
- ✅ No conflicting documentation
- ✅ Behavior preservation is the goal

### Use Forensics/defragmentation When

- ✅ Trust is low or collapsed
- ✅ Canonical source is unclear or conflicted
- ✅ Problem is project-wide
- ✅ Multiple conflicting sources exist
- ✅ Coherence restoration is the goal

---

## Common Mistakes

### Mistake 1: Refactor When Defragmentation Needed

**Symptom**: Refactoring one file while architecture is unclear
**Result**: Wasted effort, may refactor wrong thing
**Fix**: Run Forensics first to establish canonical

### Mistake 2: Defragmentation When Refactor Sufficient

**Symptom**: Full defragmentation for single code smell
**Result**: Overhead, unnecessary process
**Fix**: Use smallest sufficient intervention (refactor)

---

## Validation Checklist

- [x] Scenario A correctly uses Forge/refactor
- [x] Scenario B correctly uses Forensics/defragmentation
- [x] Decision boundary is clear
- [x] Trust level is primary discriminator
- [x] Scope (local vs project-wide) is secondary discriminator

---

## Trace File

Location: `examples/worked_traces/refactor_vs_defragmentation_trace.md`

Test: `tests/worked_examples/test_refactor_vs_defragmentation.py`
