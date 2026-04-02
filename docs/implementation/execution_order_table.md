# Execution Order Table

## Purpose

This table specifies the exact execution order for all runtime components during pipeline execution.

## Canonical Execution Order

### Phase 0: Session Initialization

| Order | Component | Action | Output |
|-------|-----------|--------|--------|
| 1 | SpecRegistry | Load all specs | SpecIndex |
| 2 | TargetResolver | Initialize with index | Ready resolver |
| 3 | TraceSelector | Initialize with index | Ready selector |
| 4 | ResidueDispatch | Initialize lens registry | Ready dispatch |
| 5 | LeverEscalation | Initialize rules | Ready escalation |
| 6 | TransitionEngine | Initialize | Ready transitions |
| 7 | RuntimeDispatcher | Initialize executors | Ready dispatcher |
| 8 | ArtifactWriter | Initialize output path | Ready writer |

### Phase 1: Pipeline Selection

| Order | Component | Action | Output |
|-------|-----------|--------|--------|
| 1 | TraceSelector | Evaluate state + trust | RouteDecision |
| 2 | TargetResolver | Resolve target | Pipeline spec |
| 3 | TransitionEngine | Execute transition | New state |

### Phase 2: Pipeline Execution

| Order | Component | Action | Output |
|-------|-----------|--------|--------|
| 1 | RuntimeDispatcher | Dispatch to executor | - |
| 2 | FamilyExecutor | Execute phase 1 | Artifact 1 |
| 3 | FamilyExecutor | Execute phase 2 | Artifact 2 |
| ... | ... | ... | ... |
| N | FamilyExecutor | Execute phase N | Artifact N |
| N+1 | FamilyExecutor | Produce route recommendation | Route recommendation |

### Phase 3: Route Execution

| Order | Component | Action | Output |
|-------|-----------|--------|--------|
| 1 | TraceSelector | Evaluate route recommendation | Next decision |
| 2 | TargetResolver | Validate target | Validated target |
| 3 | TransitionEngine | Execute transition | New state |

### Phase 4: Artifact Persistence

| Order | Component | Action | Output |
|-------|-----------|--------|--------|
| 1 | ArtifactWriter | Write artifacts | Files on disk |
| 2 | ArtifactWriter | Write provenance | Provenance file |
| 3 | ArtifactWriter | Write state snapshot | Checkpoint file |

## Execution Order by Family

### Forensics Family

| Pipeline | Phases | Order |
|----------|--------|-------|
| project_mapping | 8 phases | scope → inventory → provenance → graph → discrepancies → trust_zones → canonical → route |
| defragmentation | 7 phases | inspect → classify → choose → execute → normalize → verify → reroute |
| documentation_audit | 7 phases | doc_inventory → code_inventory → drift → gaps → misleading → report → route |
| anomaly_disambiguation | 5 phases | surface → classify → options → path → route |

### Forge Family

| Pipeline | Phases | Order |
|----------|--------|-------|
| development | 6 phases | frame → analyze → design → plan → verify → recommend |
| coding | 5 phases | understand → plan → implement → validate → recommend |
| testing | 6 phases | scope → design → execute → classify → report → recommend |
| refactor | 6 phases | map → invariants → plan → execute → validate → recommend |

### Inquiry Family

| Pipeline | Phases | Order |
|----------|--------|-------|
| research | 6 phases | frame → gather → compare → synthesize → gaps → route |
| hypothesis_generation | 6 phases | understand → generate → discriminators → select → gaps → route |
| formalization | 6 phases | concepts → relations → assumptions → define → notation → route |
| mathematics | 7 phases | problem → assumptions → derive → edge_cases → rigor → result → route |
| data_analysis | 7 phases | frame → inventory → preprocess → explore → model → report → route |

### Conduit Family

| Pipeline | Phases | Order |
|----------|--------|-------|
| documentation | 7 phases | audience → sources → outline → draft → verify → metadata → route |
| handoff_synthesis | 7 phases | scope → sources → structure → synthesize → unresolveds → provenance → steps |
| professional_writing | 6 phases | audience → outline → draft → refine → validate → deliver |
| scholarly_writing | 7 phases | genre → sources → outline → claims → draft → citations → finalize |

## Shared Authority Execution Order

### Trace Execution

| Order | Action | Condition |
|-------|--------|-----------|
| 1 | Evaluate trust assessment | Always |
| 2 | Check for trust collapse | If trust low |
| 3 | Select smallest intervention | Based on state |
| 4 | Produce route decision | Always |

### Residue Execution

| Order | Action | Condition |
|-------|--------|-----------|
| 1 | Detect suspicious surface | When anomaly present |
| 2 | Select appropriate lens | Based on anomaly type |
| 3 | Apply lens | Always |
| 4 | Produce interpretation | Always |

### Lever Execution

| Order | Action | Condition |
|-------|--------|-----------|
| 1 | Receive escalation from Trace | When Trace insufficient |
| 2 | Select evaluator | Based on problem type |
| 3 | Execute evaluator | Always |
| 4 | Make commitment/reopen decision | Based on evaluation |

## Transition Execution Order

### Within-Family Transition

| Order | Action | Validation |
|-------|--------|------------|
| 1 | Validate target pipeline exists | Check registry |
| 2 | Validate entry conditions | Check state |
| 3 | Update current_pipeline | State mutation |
| 4 | Reset phase counter | State mutation |
| 5 | Return success | - |

### Cross-Family Transition

| Order | Action | Validation |
|-------|--------|------------|
| 1 | Validate target family exists | Check registry |
| 2 | Validate transition legal | Check dependency law |
| 3 | Update current_family | State mutation |
| 4 | Reset current_pipeline | State mutation |
| 5 | Record in route_history | State mutation |
| 6 | Return success | - |

## Error Handling Order

### Phase Failure

| Order | Action | Output |
|-------|--------|--------|
| 1 | Catch exception | - |
| 2 | Record error in state | state.errors appended |
| 3 | Halt phase execution | - |
| 4 | Route to error handler | Based on severity |

### Route Resolution Failure

| Order | Action | Output |
|-------|--------|--------|
| 1 | Detect invalid target | - |
| 2 | Record resolution error | state.errors appended |
| 3 | Attempt fallback target | Default route |
| 4 | If fallback fails → Forensics | Safety reroute |

## Checkpoint Order

### State Checkpoint

| Order | Action | Frequency |
|-------|--------|-----------|
| 1 | Serialize state | After each pipeline |
| 2 | Write artifacts | After each pipeline |
| 3 | Write route history | After each pipeline |
| 4 | Write timestamp | Always |

## Performance Order

### Optimization Priority

1. **Spec loading**: Cache after first load
2. **Target resolution**: O(1) lookup with index
3. **Artifact writing**: Batch writes when possible
4. **State mutations**: Minimize copies
