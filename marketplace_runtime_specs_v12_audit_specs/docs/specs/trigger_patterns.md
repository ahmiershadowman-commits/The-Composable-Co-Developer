# Trigger Patterns Specification

## Trigger ownership model

### Trace owns
- routine micro-checks
- smallest-sufficient intervention choice
- selector execution
- ordinary routing supervision

### Residue owns
- suspicious-surface interpretation
- lens-based first responses
- anomaly/misfit/missingness/tension shaping

### Lever owns
- evaluator invocation
- explicit adjudication
- escalation
- commitment/reopen decisions

### Transition engine owns
- actual phase/pipeline/family transitions
- legality enforcement
- forensics reset execution

## Trace-level triggers

### phase_mismatch
Triggered when:
- current phase no longer fits the dominant problem
- a phase is continuing only by momentum

Expected response:
- phase pivot if possible
- sibling pipeline shift if phase mismatch implies pipeline mismatch

### confidence_support_mismatch
Triggered when:
- output confidence exceeds support quality
- commitment pressure outruns evidence

Expected response:
- primitive or evaluator before commitment
- reroute to Inquiry when support must be deepened

### branch_sprawl
Triggered when:
- too many live options remain without real discriminators

Expected response:
- primitive `trim`
- evaluator `discriminator_evaluator`

### trust_collapse
Triggered when:
- canonical state is uncertain
- docs, repo, runtime, or assumptions conflict materially

Expected response:
- cross-family reroute to Forensics
- sometimes direct `forensics_reset`

### artifact_shape_drift
Triggered when:
- artifact structure no longer matches expected form

Expected response:
- local cleanup if minor
- Refactor or Defragmentation if structural

## Residue-level triggers

### misfit_detected
Expected first response:
- `misfit` lens
- primitive `open`
- primitive `locate`

### absence_detected
Expected first response:
- `absence` lens
- primitive `reread`
- primitive `separate`

### tension_detected
Expected first response:
- `tension` lens
- primitive `hold`
- primitive `shift`

### warp_detected
Expected first response:
- `warp` lens
- primitive `center`
- primitive `locate`

### offset_detected
Expected first response:
- `offset` lens
- primitive `separate`
- primitive `reread`

## Lever-level triggers

### contradiction_requires_adjudication
Expected response:
- `contradiction_evaluator`

### support_requires_adjudication
Expected response:
- `support_evaluator`

### frame_requires_adjudication
Expected response:
- `frame_evaluator`

### discriminator_required
Expected response:
- `discriminator_evaluator`

### shape_requires_adjudication
Expected response:
- `artifact_shape_evaluator`

## Forbidden shortcuts
- invoking Lever before Trace has attempted smallest-sufficient handling
- jumping to cross-family reroute when a legal local intervention remains
- using motifs as direct triggers
- using Residue as a substitute for explicit evaluator adjudication
- rendering unsupported claims in Conduit without rerouting
- continuing Forge or Inquiry after trust collapse without Forensics
