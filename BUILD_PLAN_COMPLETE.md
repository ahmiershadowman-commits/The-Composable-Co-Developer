# Complete Build Plan

## Purpose
This document provides a prioritized, sequential build plan to complete all missing components identified in the `marketplace_runtime_specs_v12_audit_specs` audit.

## Build Order Principle
Build in dependency order. Each task unlocks the next. Do not skip ahead.

---

## Priority 0: Core Execution Gaps

### Task 0.1: Defragmentation Executor Implementation
**Status**: NOT STARTED  
**Priority**: CRITICAL  
**Dependencies**: None (runtime spine exists)  
**Unlocks**: Full Forensics family, vertical slice completeness

**Scope**:
- Implement `ForensicsExecutor.execute_defragmentation()` method
- 7 phases matching `entrypoints/Forensics/pipelines/defragmentation/pipeline.yaml`:
  1. `inspect_state` - fragmentation snapshot
  2. `classify_entropy` - entropy classification (tidy/consolidate/repair/anchor)
  3. `choose_method` - smallest sufficient method selection
  4. `execute_method` - apply tidy/consolidate/repair/anchor
  5. `normalize_metadata_and_provenance` - alignment record
  6. `verify_restored_coherence` - trust reassessment
  7. `finalize_or_reroute` - route recommendation

**Artifacts to produce**:
- `fragmentation_snapshot`
- `entropy_classification`
- `chosen_method`
- `residue_disposition_ledger`
- `changed_structure_map`
- `metadata_normalization_record`
- `trust_reassessment_note`
- `route_recommendation`

**Files to modify**:
- `entrypoints/Forensics/executors.py` - add `execute_defragmentation()` method
- `runtime/execution/dispatcher.py` - wire up defragmentation call

**Tests to add**:
- `tests/runtime/test_defragmentation_executor.py`

---

## Priority 1: Remaining Forensics Executors

### Task 1.1: Documentation Audit Executor
**Status**: NOT STARTED  
**Priority**: HIGH  
**Dependencies**: Task 0.1 complete  
**Unlocks**: Full Forensics audit capability

**Scope**:
- Implement `ForensicsExecutor.execute_documentation_audit()` method
- Audit documentation against actual code state
- Identify drift, gaps, and misleading claims

**Artifacts to produce**:
- `documentation_inventory`
- `code_state_inventory`
- `drift_ledger`
- `gap_analysis`
- `misleading_claims_ledger`
- `audit_report`
- `route_recommendation`

**Files to modify**:
- `entrypoints/Forensics/executors.py`

---

### Task 1.2: Anomaly Disambiguation Executor
**Status**: NOT STARTED  
**Priority**: HIGH  
**Dependencies**: Task 0.1 complete  
**Unlocks**: Full Forensics anomaly handling

**Scope**:
- Implement `ForensicsExecutor.execute_anomaly_disambiguation()` method
- Surface anomalies, classify type, propose disambiguation paths

**Artifacts to produce**:
- `anomaly_catalog`
- `anomaly_classification` (misfit/absence/tension/warp/offset)
- `disambiguation_options`
- `recommended_path`
- `route_recommendation`

**Files to modify**:
- `entrypoints/Forensics/executors.py`

---

## Priority 2: Architecture Documentation Layer

### Task 2.1: Motif Layer
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Semantic conditioning layer

**Scope**:
- Create `shared/motifs/README.md` - motif layer rationale
- Create `shared/motifs/registry.yaml` - motif registry
- Create first motif files:
  - `unfinished_proof.yaml`
  - `watershed.yaml`
  - `tension_point.yaml`
  - `absence_signal.yaml`
- Create `docs/architecture/motif_layer_rationale.md`

**Files to create**:
- `shared/motifs/README.md`
- `shared/motifs/registry.yaml`
- `shared/motifs/unfinished_proof.yaml`
- `shared/motifs/watershed.yaml`
- `shared/motifs/tension_point.yaml`
- `shared/motifs/absence_signal.yaml`
- `docs/architecture/motif_layer_rationale.md`

---

### Task 2.2: Runtime Execution Semantics
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: Task 0.1 complete (defragmentation executor)  
**Unlocks**: Clear execution order understanding

**Scope**:
- Document execution order table
- Document runtime semantics

**Files to create**:
- `docs/implementation/runtime_execution_semantics.md`
- `docs/implementation/execution_order_table.md`

---

### Task 2.3: Artifact Schema Layer
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Artifact contract clarity

**Scope**:
- Document artifact contract
- Create artifact schema files

**Files to create**:
- `docs/architecture/artifact_contract.md`
- `runtime/schemas/artifacts/README.md`
- `runtime/schemas/artifacts/inventory_ledger.yaml`
- `runtime/schemas/artifacts/trust_assessment.yaml`
- `runtime/schemas/artifacts/route_decision.yaml`

---

### Task 2.4: Unresolveds Ledger
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Explicit unresolved tracking

**Scope**:
- Document unresolveds ledger pattern
- Add to ExecutionState model if needed

**Files to create**:
- `docs/architecture/unresolveds_ledger.md`

---

### Task 2.5: Acceptance Matrix
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: All executors complete  
**Unlocks**: Clear acceptance criteria

**Scope**:
- Document acceptance matrix for each family/pipeline

**Files to create**:
- `docs/implementation/acceptance_matrix.md`

---

### Task 2.6: Hook and Interface Contract
**Status**: NOT STARTED  
**Priority**: LOW (deferred per spine scope)  
**Dependencies**: None  
**Unlocks**: Hook system clarity (future work)

**Scope**:
- Document hook contract (PreToolUse, PostToolUse, etc.)
- Document interface contracts

**Files to create**:
- `docs/implementation/hook_and_interface_contract.md`

---

### Task 2.7: Operator Expansion
**Status**: NOT STARTED  
**Priority**: LOW  
**Dependencies**: None  
**Unlocks**: More operator interventions

**Scope**:
- Expand operator registry beyond clarify/distill
- Add operators: `compare`, `extract`, `reframe`, `triangulate`

**Files to create**:
- `shared/operators/README.md`
- `shared/operators/compare.yaml`
- `shared/operators/extract.yaml`
- `shared/operators/reframe.yaml`
- `shared/operators/triangulate.yaml`
- Update `shared/operators/registry.yaml`

---

### Task 2.8: Taskboard Manifest
**Status**: NOT STARTED  
**Priority**: LOW  
**Dependencies**: None  
**Unlocks**: Task tracking

**Scope**:
- Create taskboard manifest YAML

**Files to create**:
- `docs/implementation/taskboard_manifest.yaml`

---

## Priority 3: Worked Trace Expansion

### Task 3.1: Inquiry Trace
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: Inquiry executor complete (DONE)  
**Unlocks**: Inquiry validation

**Scope**:
- Create worked trace: Forensics → Inquiry → Conduit

**Files to create**:
- `examples/worked_traces/inquiry_trace.md`
- `tests/worked_examples/test_inquiry_trace.py`

---

### Task 3.2: Conduit Fallback Trace
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: Conduit executor complete (DONE)  
**Unlocks**: Conduit validation

**Scope**:
- Create worked trace: Trust collapse → Forensics → Conduit

**Files to create**:
- `examples/worked_traces/conduit_fallback_trace.md`
- `tests/worked_examples/test_conduit_fallback_trace.py`

---

### Task 3.3: Residue → Trace → Lever Trace
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: All shared authorities complete (DONE)  
**Unlocks**: Authority interaction validation

**Scope**:
- Create worked trace showing full authority escalation

**Files to create**:
- `examples/worked_traces/authority_escalation_trace.md`
- `tests/worked_examples/test_authority_escalation_trace.py`

---

### Task 3.4: Forge Refactor vs Defragmentation Trace
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: Task 0.1 complete  
**Unlocks**: Clear refactor/defragmentation boundary

**Scope**:
- Create worked trace showing when to use each

**Files to create**:
- `examples/worked_traces/refactor_vs_defragmentation_trace.md`
- `tests/worked_examples/test_refactor_vs_defragmentation.py`

---

## Priority 4: Boundary Rules

### Task 4.1: Primitive/Operator/Evaluator Boundaries
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Clear layer separation

**Scope**:
- Document boundary rules to prevent layer bleed

**Files to create**:
- `docs/architecture/action_layer_boundaries.md`

---

### Task 4.2: Method Target Legality
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Clear method scoping

**Scope**:
- Document `method:<name>` legality rules

**Files to create**:
- `docs/architecture/method_target_legality.md`

---

### Task 4.3: Artifact Update Semantics
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Clear artifact update rules

**Scope**:
- Document replace/append/merge/version semantics

**Files to create**:
- `docs/architecture/artifact_update_semantics.md`

---

### Task 4.4: Shared Authority Execution Order
**Status**: NOT STARTED  
**Priority**: MEDIUM  
**Dependencies**: None  
**Unlocks**: Clear authority order

**Scope**:
- Document Trace → Residue → Lever order explicitly

**Files to create**:
- `docs/architecture/shared_authority_order.md`

---

## Priority 5: Verification

### Task 5.1: Full Test Suite
**Status**: NOT STARTED  
**Priority**: CRITICAL (after all implementation)  
**Dependencies**: All above tasks complete  
**Unlocks**: Confidence in bundle

**Scope**:
- Run full pytest suite
- Fix any failures
- Verify all 29+ tests pass

**Command**:
```bash
python -m pytest tests -v
```

---

### Task 5.2: Vertical Slice Validation
**Status**: NOT STARTED  
**Priority**: CRITICAL (after all implementation)  
**Dependencies**: Task 0.1 complete  
**Unlocks**: End-to-end confidence

**Scope**:
- Run vertical slice with full defragmentation
- Verify 0 errors

**Command**:
```bash
python tools/run_vertical_slice.py
```

---

### Task 5.3: Bundle Validation
**Status**: NOT STARTED  
**Priority**: CRITICAL (after all implementation)  
**Dependencies**: All tasks complete  
**Unlocks**: Handoff readiness

**Scope**:
- Run bundle validator
- Verify inventory matches BUILD_CONTRACT.md

**Command**:
```bash
python tools/validate_bundle.py
```

---

## Summary: Task Count by Priority

| Priority | Task Count | Description |
|----------|------------|-------------|
| 0 | 1 | Defragmentation executor (CRITICAL) |
| 1 | 2 | Remaining Forensics executors |
| 2 | 8 | Architecture documentation layer |
| 3 | 4 | Worked trace expansion |
| 4 | 4 | Boundary rules documentation |
| 5 | 3 | Verification (tests, slice, bundle) |

**Total**: 22 tasks

---

## Build Checklist

- [ ] **0.1** Defragmentation executor
- [ ] **1.1** Documentation audit executor
- [ ] **1.2** Anomaly disambiguation executor
- [ ] **2.1** Motif layer
- [ ] **2.2** Runtime execution semantics
- [ ] **2.3** Artifact schema layer
- [ ] **2.4** Unresolveds ledger
- [ ] **2.5** Acceptance matrix
- [ ] **2.6** Hook and interface contract
- [ ] **2.7** Operator expansion
- [ ] **2.8** Taskboard manifest
- [ ] **3.1** Inquiry trace
- [ ] **3.2** Conduit fallback trace
- [ ] **3.3** Residue → Trace → Lever trace
- [ ] **3.4** Forge refactor vs defragmentation trace
- [ ] **4.1** Primitive/operator/evaluator boundaries
- [ ] **4.2** Method target legality
- [ ] **4.3** Artifact update semantics
- [ ] **4.4** Shared authority execution order
- [ ] **5.1** Full test suite
- [ ] **5.2** Vertical slice validation
- [ ] **5.3** Bundle validation

---

## Update Time
2026-03-25
