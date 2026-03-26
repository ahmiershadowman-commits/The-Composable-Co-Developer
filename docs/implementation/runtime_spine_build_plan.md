# Runtime Spine Build Plan

## Purpose

Implement the minimum live kernel that can:
- load the marketplace spec bundle
- validate schema and inventory
- resolve canonical targets
- execute Trace
- dispatch Residue lenses
- escalate to Lever
- transition legally across phase/pipeline/family boundaries
- emit artifacts and provenance
- run one real vertical slice end-to-end

This is the build priority above all family-specific runtime work.

## Scope

### In scope
- runtime state objects
- spec registry
- target resolver
- Trace execution
- Residue dispatch
- Lever dispatch
- transition engine
- artifact/provenance emission
- runtime-aware validation
- one executable vertical slice

### Out of scope for this phase
- broad MCP implementation
- broad hook implementation
- UI
- experimental pipeline execution
- full adapter surface
- family-wide feature completeness before the spine is proven

## Implementation order

### 1. Freeze runtime scope
Create:
- `docs/implementation/runtime_spine_scope.md`

Must state:
- what the spine is
- what it is not
- what is deferred

### 2. Build package scaffolding
Create or fill:
- `runtime/__init__.py`
- `runtime/state/`
- `runtime/registry/`
- `runtime/methodology/`
- `runtime/trace/`
- `runtime/residue/`
- `runtime/lever/`
- `runtime/execution/`
- `runtime/artifacts/`
- `runtime/errors/`

### 3. Define runtime state models
Implement:
- `runtime/state/models.py`

Required models:
- `RuntimeContext`
- `ExecutionState`
- `RouteDecision`
- `ArtifactRecord`
- `TrustAssessment`

### 4. Build the registry layer
Implement:
- `runtime/registry/loader.py`
- `runtime/registry/index.py`
- `runtime/registry/validators.py`

Required capabilities:
- discover all spec files
- build family/pipeline inventory
- load selectors
- load route maps
- load primitives/operators/evaluators/lenses
- validate inventory and schema consistency

### 5. Build canonical target resolution
Implement:
- `runtime/methodology/targets.py`
- `runtime/methodology/target_resolver.py`

Must resolve:
- `primitive:<name>`
- `operator:<name>`
- `evaluator:<name>`
- `method:<name>`
- `pipeline:<Family>/<pipeline_id>`
- `family:<Family>`
- `authority:<Trace|Lever|Residue>`
- `forensics_reset`

### 6. Build Trace
Implement:
- `runtime/trace/checklist.py`
- `runtime/trace/rubric.py`
- `runtime/trace/selector.py`
- `runtime/trace/intervention.py`
- `runtime/trace/planner.py`

Trace must:
- load selectors
- evaluate smallest-sufficient intervention
- emit structured `RouteDecision`
- remain family-agnostic

### 7. Build Residue dispatch
Implement:
- `runtime/residue/registry.py`
- `runtime/residue/dispatch.py`

Residue must:
- load lenses and trigger map
- recommend smallest first response
- preserve oddity before forced reroute

### 8. Build Lever
Implement:
- `runtime/lever/registry.py`
- `runtime/lever/evaluators.py`
- `runtime/lever/escalation.py`
- `runtime/lever/commitment.py`

Lever must:
- dispatch evaluators
- return structured evaluation results
- support escalation, commitment, and reopen behaviors

### 9. Build transition engine
Implement:
- `runtime/execution/transitions.py`
- `runtime/execution/dispatcher.py`

Must support:
- phase pivot
- sibling pipeline shift
- cross-family reroute
- authority target handling
- forensics reset
- method target handling

### 10. Build artifact and provenance layer
Implement:
- `runtime/artifacts/writer.py`
- `runtime/artifacts/provenance.py`
- `runtime/artifacts/logging.py`

Must write:
- artifacts
- route history
- provenance records
- unresolveds
- route recommendations

### 11. Build the first vertical slice
Implement:
- `tools/run_vertical_slice.py`

Required slice:
- `Forensics/project_mapping`
- `Forensics/defragmentation`
- `Forensics/project_mapping`
- `Forge/development`
- `Forge/coding`
- `Forge/testing`

### 12. Add runtime-aware tests
Create:
- `tests/runtime/`

Test types:
- registry load tests
- target resolution tests
- selector execution tests
- transition legality tests
- vertical-slice tests

## Calibration checkpoints

### Checkpoint 1 — Registry
Can the runtime load and index the entire bundle?

### Checkpoint 2 — Target resolution
Can every runtime target resolve to a typed object or structured error?

### Checkpoint 3 — Trace
Can Trace choose a smallest-sufficient action from state + selector + route map?

### Checkpoint 4 — Residue
Can suspicious-surface triggers become structured interventions?

### Checkpoint 5 — Lever
Can Trace escalate and get a structured result back?

### Checkpoint 6 — Transitions
Can the system move legally between phases, pipelines, and families?

### Checkpoint 7 — Artifacts
Do real files get written for route decisions, provenance, and outputs?

### Checkpoint 8 — Vertical slice
Does the first slice run end-to-end without architecture improvisation?

## Merge gate

Do not widen into family completeness until:
- all eight checkpoints pass
- the vertical slice works
- runtime-aware tests pass
