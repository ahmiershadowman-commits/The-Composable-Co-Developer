# Decorative Process Audit

## Purpose

This audit asks whether the current package has become a process-heavy architecture
that risks controlling an LLM like a puppet rather than scaffolding it into more
reliable research and development behavior.

## Bottom-line judgment

The package is **not yet a puppet-control architecture**, but it is at risk of
becoming one if more control layers are added without first proving that the
runtime spine and first vertical slices materially improve outcomes.

The strongest parts of the design are the ones that:
- preserve autonomy,
- make routing explicit,
- improve trust handling,
- improve artifact/provenance discipline,
- and reduce fresh-state drift.

The weakest parts are the ones that could drift into decorative process if they
are elaborated further without empirical payoff.

## Most justified layers
- Forensics as the only deep truth-establishing entry
- Trace as smallest-sufficient controller
- Lever as bounded evaluator/escalation layer
- Residue as suspicious-surface lens layer
- family separation between truth, build/change, inquiry, and rendering

## Main overcomplexity risks
- excessive operator/evaluator proliferation
- too many experimental/live pipelines before runtime proof
- motifs becoming hidden control logic
- tests expanding faster than executable runtime

## Recommendation
Treat the architecture as:
- scaffold-first
- proof-before-expansion
- autonomy-preserving
- truth-first
- artifact-disciplined
