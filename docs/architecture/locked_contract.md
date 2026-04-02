# Locked Contract

This file records the architecture decisions currently treated as load-bearing.

## Non-negotiables

- Forensics is the only deep ground-truth entrypoint.
- Trace is the traveling micro-supervisory controller.
- Lever is evaluator / escalation / commitment authority.
- Residue is a shared suspicious-surface lens library, not a pipeline family.
- Defragmentation is a Forensics-owned downstream pipeline.
- Pipelines are end-to-end micro-methodologies with exits, reroutes, cleanup, and artifact schemas.
- Entry families remain:
  - Forensics
  - Forge
  - Inquiry
  - Conduit

## Canonical grammar

- Pipelines use the canonical schema in `runtime/schemas/pipeline.yaml`.
- Targets use the canonical grammar in `runtime/methodology/target_grammar.yaml`.
- Aliases are frontmatter only; canonical ids are runtime-facing.

## Status

This contract reflects the normalized bundle state, not an earlier pre-normalization snapshot.
