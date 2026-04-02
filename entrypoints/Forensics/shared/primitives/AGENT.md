# AGENT GUIDE — shared/primitives/

Role note: Primitive inventory. Low-cost reusable interventions only.

## Build this directory exactly

Subdirectories that must exist:
- `metacognitive/`
- `reasoning/`

Files that must exist in this directory:
- `registry.yaml`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Trace
- Route policies
- Pipelines through smallest-sufficient interventions

## Immediate child inventory

- `metacognitive/`
- `reasoning/`
- `registry.yaml`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.