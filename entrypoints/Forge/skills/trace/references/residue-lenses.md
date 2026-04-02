# Residue Lenses

Residue is the suspicious-surface lens library. It is an authority, not a pipeline family. Consult Residue when a surface feels smoothed, incomplete, suspicious, or structurally odd — when anomaly signals appear that Trace cannot resolve with a primitive.

**Forbidden**: Do not treat Residue as a generic analysis pass. Do not use it as a substitute for explicit evaluator adjudication. Do not invoke it before Trace has evaluated.

## Lens registry

### misfit
**Trigger**: Something doesn't fit the surrounding structure in a way that can't be explained
**What it surfaces**: Elements that violate expected pattern, scale, or category
**Typical first response**: primitive `open`, primitive `locate`
**Escalation**: If misfit source is identified, Trace routes recommendation; if misfit requires adjudication, escalate to Lever

### absence
**Trigger**: Something that should be present is conspicuously missing
**What it surfaces**: Expected components, constraints, cases, or caveats that are absent
**Typical first response**: primitive `reread`, primitive `separate`
**Escalation**: Surface the absence explicitly; may require Inquiry to fill the gap

### tension
**Trigger**: Two active claims or surfaces materially disagree
**What it surfaces**: The specific disagreement, its materiality, and whether local resolution is possible
**Typical first response**: primitive `hold`, primitive `shift`
**Escalation**: If adjudication is needed, → Lever `contradiction_evaluator`

### warp
**Trigger**: The frame or scope of analysis has drifted from what was intended
**What it surfaces**: How the current lens or frame has shifted; what the intended scope was
**Typical first response**: primitive `center`, primitive `locate`
**Escalation**: Trace incorporates and reanchors; if frame itself is wrong → Lever `frame_evaluator`

### offset
**Trigger**: The analysis is systematically displaced — right category, wrong instance; right pattern, wrong scale
**What it surfaces**: The direction and magnitude of the offset from the correct target
**Typical first response**: primitive `separate`, primitive `reread`
**Escalation**: Trace corrects offset; if offset is structural → Lever `artifact_shape_evaluator`

### signal
**Trigger**: A weak but persistent signal is being drowned out by louder but less meaningful content
**What it surfaces**: The suppressed signal and why it may be load-bearing
**Typical first response**: primitive `open`, operator `extract`
**Escalation**: Trace weighs signal; if signal implies frame error → Lever `frame_evaluator`

### burden
**Trigger**: An assumption is doing more work than it can support
**What it surfaces**: The overloaded assumption and what would fail if it were wrong
**Typical first response**: primitive `press`, primitive `hold`
**Escalation**: If burden is critical → Lever `support_evaluator`

### edge
**Trigger**: A boundary condition or edge case has been implicitly excluded
**What it surfaces**: The excluded case and whether it would change the result
**Typical first response**: primitive `open`, primitive `bind`
**Escalation**: Trace decides whether edge case is material; if it is → Inquiry `research` or `formalization`

## Execution order

Residue is consulted in parallel with or after Trace evaluation, never before.

```
Trace evaluates
  → detects suspicious surface
    → consult Residue for lens interpretation
      → Residue applies lens
        → returns interpretation
          → Trace incorporates into route decision
```
