# Missing Components Specification

Last updated: 2026-03-26

## Resolved in this sprint

The following items from the original spec were completed during the plugin build pass:

| Item | Status | Where |
|------|--------|-------|
| Plugin manifest | ✅ Built | `.claude-plugin/plugin.json` |
| Skills SKILL.md for all 4 families | ✅ Built | `skills/forensics/`, `skills/forge/`, `skills/inquiry/`, `skills/conduit/` |
| Trace skill (metacognitive supervisor) | ✅ Built | `skills/trace/SKILL.md` |
| Portable pipeline runner | ✅ Built | `scripts/run_pipeline.sh` |
| Hooks (Trace ambient + Forensics gate) | ✅ Built | `hooks/hooks.json` |
| Error recovery fallbacks in all skills | ✅ Built | All 4 family SKILL.md files |
| Artifact schema YAML files | ✅ Built | `runtime/schemas/artifacts/*.yaml` |
| Acceptance matrices per family | ✅ Built | `skills/*/references/acceptance-matrix.md` |
| Artifact contracts per family | ✅ Built | `skills/*/references/artifacts.md` |
| Entry.skill.yaml for Forge, Inquiry, Conduit | ✅ Built | `entrypoints/*/entry.skill.yaml` |
| Legacy skills/*.py relocated | ✅ Done | `runtime/skills_runners/` (stubs left in skills/) |
| Forensics executor real filesystem I/O | ✅ Built | `entrypoints/Forensics/executors.py` |
| Operators: reframe, triangulate, compare, extract | ✅ Present | `shared/operators/*.yaml` |

## Still missing (genuine gaps)

### 1. Motif layer
The motif layer is referenced in `entry.skill.yaml` files and the intervention stack spec but has no standalone files yet.
Need:
- `shared/motifs/README.md`
- `shared/motifs/registry.yaml`
- Per-motif YAML files (tight-loop, minimal-footprint, unfinished-proof, watershed, zero-in)
- `docs/architecture/motif_layer_rationale.md`

### 2. Runtime execution semantics documentation
Need:
- `docs/implementation/runtime_execution_semantics.md`
- `docs/implementation/execution_order_table.md`

### 3. Unresolveds ledger format
The `unresolveds_and_risks.yaml` artifact is referenced in Conduit pipelines but has no schema file.
Need:
- `runtime/schemas/artifacts/unresolveds_and_risks.yaml`
- `docs/architecture/unresolveds_ledger.md`

### 4. Hook and interface contract documentation
Need:
- `docs/implementation/hook_and_interface_contract.md` — documents the Trace + Forensics gate hook behavior for operators

### 5. Worked trace expansion
The `examples/worked_traces/` directory contains one Forensics trace. Additional traces would make the methodology teachable.
Need:
- Inquiry/research trace
- Conduit/handoff_synthesis fallback trace
- Residue → Trace → Lever intervention trace
- Forge refactor vs Defragmentation decision trace

### 6. Taskboard manifest
Need:
- `docs/implementation/taskboard_manifest.yaml` — machine-readable status of all components

### 7. data_analysis pipeline executor
The `Inquiry/data_analysis` pipeline is marked experimental. The executor exists as a stub.
Need: `execute_data_analysis()` in `entrypoints/Inquiry/executors.py` wired to dispatcher.

### 8. Operator README
Need: `shared/operators/README.md` explaining the operator class system and how to call operators.

## Not missing (previously listed, now confirmed present)

- Artifact schema layer: `runtime/schemas/artifacts/` has YAML schemas
- Acceptance matrix: per-family `references/acceptance-matrix.md` in all 4 skills
- Operator expansion: 6 core operators present (clarify, distill, compare, extract, reframe, triangulate)
