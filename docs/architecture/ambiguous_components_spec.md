# Ambiguous Components Specification

## 1. Motif mechanics
Still ambiguous whether motifs are:
- inference-layer semantic conditioning
- runtime-side weighting
- or hybrid

Recommended direction:
- hybrid

## 2. Primitive / operator / evaluator boundaries
Need a clean boundary rules doc to prevent layer bleed.

## 3. Method target legality
Need to explicitly lock:
- `method:<name>` valid only inside the active pipeline and only if declared there

## 4. Artifact update semantics
Need to lock whether artifacts:
- replace
- append
- merge
- version

## 5. Shared authority execution order
Need to explicitly lock:
- Trace first
- Residue when suspicious surface appears
- Lever when Trace + Residue are insufficient

## 6. Experimental promotion criteria
Need explicit, testable promotion gates.
