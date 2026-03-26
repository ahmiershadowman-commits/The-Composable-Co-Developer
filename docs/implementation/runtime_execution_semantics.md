# Runtime Execution Semantics

## Purpose

This document specifies how the marketplace runtime executes pipelines, manages state transitions, and coordinates between components.

## Execution Model

### Overview

The runtime follows a **deterministic phase-order execution** model:

1. Pipelines execute phases in declared order
2. Each phase produces specific artifacts
3. State transitions occur between phases
4. Route decisions determine next target

### Execution Flow

```
User Prompt → Selector → Target Resolver → Pipeline Executor
                                           ↓
                                    Phase 1
                                           ↓
                                    Phase 2
                                           ↓
                                      ...
                                           ↓
                                    Final Phase
                                           ↓
                                    Route Decision → Next Target
```

## Component Responsibilities

### Selector

**Responsibility**: Determine which pipeline/family should handle current state

**Input**: 
- Current execution state
- Trust assessment
- Available pipeline inventory

**Output**: 
- Route decision with target

**Execution timing**: Before each pipeline invocation

### Target Resolver

**Responsibility**: Validate and resolve route targets to executable pipelines

**Input**: 
- Route target string (e.g., `pipeline:Forensics/project_mapping`)
- Spec index with registered pipelines

**Output**: 
- Resolved pipeline spec or error

**Validation rules**:
- Target must match canonical grammar
- Pipeline must exist in registry
- Entry conditions must be satisfiable

### Pipeline Executor

**Responsibility**: Execute pipeline phases in order

**Input**:
- Pipeline spec
- Execution state
- Context data

**Output**:
- Updated state with artifacts
- Route recommendation

**Execution rules**:
- Phases execute in declared order
- Each phase must complete before next
- Phase failures halt execution
- Artifacts accumulate in state

## State Management

### ExecutionState Lifecycle

```
SessionStart → Initial State → [Pipeline Execution] → Final State → SessionEnd
                    ↑                    ↑                     ↑
                    │                    │                     │
              Family selected      Artifacts            Route decision
                                 accumulated            recorded
```

### State Transitions

State transitions occur at:

1. **Pipeline entry**: `current_pipeline` set
2. **Phase completion**: Artifact added to `state.artifacts`
3. **Route decision**: `route_history` updated
4. **Family transition**: `current_family` changed
5. **Trust update**: `trust_assessment` modified

### Artifact Accumulation

Artifacts are immutable once added:

```python
state.add_artifact("name", data)  # Adds to state.artifacts
# Cannot modify or remove after addition
```

## Route Decision Execution

### Route Decision Structure

```yaml
action: ROUTE  # or CROSS_FAMILY_REROUTE, PHASE_PIVOT, etc.
target: "pipeline:Forensics/project_mapping"
intervention_band: CROSS_FAMILY_REROUTE
reason: "State grounded - build work can proceed"
family: FORGE  # target family
```

### Route Execution

1. **Transition engine** receives route decision
2. **Validates** target is legal from current state
3. **Updates** state (family, pipeline, phase)
4. **Returns** transition result with success flag

### Legal Transitions

| From | To | Allowed? | Condition |
|------|-----|----------|-----------|
| Forensics | Forge | Yes | Trust established |
| Forensics | Inquiry | Yes | Questions remain |
| Forensics | Conduit | Yes | Synthesis needed |
| Forge | Forensics | Yes | Trust collapsed |
| Forge | Inquiry | Yes | Investigation needed |
| Inquiry | Conduit | Yes | Ready to communicate |
| Conduit | Forensics | Yes | Trust issues detected |

## Intervention Selection

### Smallest Sufficient Intervention Principle

When multiple interventions could address a situation, select the least invasive:

```
Primitive < Operator < Evaluator < Pipeline Reroute < Cross-Family Reroute
```

### Intervention Band Hierarchy

1. **Local** (within phase): Primitive, operator
2. **Phase** (within pipeline): Phase pivot
3. **Pipeline** (within family): Pipeline switch
4. **Cross-family**: Reroute to different family

### Selection Logic

```
If problem is local → Apply primitive/operator
Else if problem is phase-specific → Phase pivot
Else if problem is pipeline-specific → Pipeline switch
Else → Cross-family reroute
```

## Error Handling

### Phase Failure

When a phase fails:

1. **Record error** in `state.errors`
2. **Halt execution** of current pipeline
3. **Route to appropriate handler**:
   - Minor error → Continue with warning
   - Major error → Reroute to Forensics
   - Critical error → Stop execution

### State Recovery

State can be recovered from checkpoints:

```yaml
checkpoint:
  state_snapshot: {...}
  artifacts: {...}
  route_history: [...]
```

## Execution Guarantees

### Determinism

Given:
- Same initial state
- Same pipeline spec
- Same context

The runtime will produce:
- Same artifact sequence
- Same final state
- Same route decisions

### Isolation

Each pipeline execution is isolated:

- Artifacts from one pipeline don't interfere with another
- State mutations are explicit and logged
- Route history provides full audit trail

### Termination

All executions terminate:

- Pipelines have finite phases
- Route decisions always produce a target
- No infinite loops in normal operation

## Performance Characteristics

### Time Complexity

- **Pipeline execution**: O(phases)
- **Route resolution**: O(1) with spec index
- **Artifact lookup**: O(1) with hash map

### Space Complexity

- **State size**: O(artifacts)
- **Route history**: O(route_decisions)
- **Checkpoint size**: O(state + artifacts)

## Monitoring and Observability

### Execution Logging

All executions are logged:

```yaml
log_entry:
  timestamp: "2026-03-25T10:30:00Z"
  pipeline: "Forensics/project_mapping"
  phase: "inventory_artifacts"
  artifacts_produced: ["inventory_ledger"]
  route_decision: "pipeline:Forensics/defragmentation"
```

### Metrics

Key metrics to track:

- Pipeline execution time
- Phase completion rate
- Route decision distribution
- Error frequency by type
