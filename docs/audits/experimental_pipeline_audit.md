# Experimental Pipeline Audit

## Scope
This audit evaluates whether the currently marked experimental pipelines should be promoted to core or remain parked.

## Pipelines reviewed

### Forensics
- `label_shift_correction`
- `introspection_audit`

### Inquiry
- `prompt_order_optimization`
- `human_hint_integration`

## Recommendation
Keep all four as **experimental** for now.

## Reasoning

### 1. They are not yet structurally necessary for the core marketplace
The core marketplace already has a complete and internally coherent path for:
- truth establishment
- entropy reduction
- build/change
- evidence/explanation
- communication/handoff

These four pipelines do not currently close a core architectural gap.

### 2. They are frontier-specialized rather than universally load-bearing
Each one addresses a narrower family of situations:
- label-marginal mismatch
- introspective / interpretability audit
- prompt-order sensitivity
- human hint hybridization

That makes them good candidates for incubation but not yet promotion.

### 3. They are not yet metabolized into the main family routing logic
They are inventoried properly, but they are still not driving the default route grammar for their families.
That is correct for their current maturity.

## Promotion criteria
Promote only when all of the following are true:
- repeated worked examples show the pipeline is not niche-only
- it becomes a common first-class sibling shift from core pipelines
- its evaluator, primitive, and operator dependencies are stable
- its outputs become regular inputs to other families
- it no longer behaves like a research appendage to the architecture

## Current action
- keep `status: experimental`
- do not place in live selector pipeline scopes
- keep route-map visibility through `experimental_pipelines`
- revisit after worked trace coverage expands
