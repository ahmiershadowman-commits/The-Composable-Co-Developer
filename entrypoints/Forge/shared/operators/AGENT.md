# AGENT GUIDE — shared/operators/

Role note: Operators heavier than primitives, lighter than family reroutes.

## Build this directory exactly

Files that must exist in this directory:
- `clarify.yaml`
- `distill.yaml`
- `invocation_spectrum.yaml`
- `registry.yaml`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Pipelines
- Trace/Lever escalation boundary

## Immediate child inventory

- `clarify.yaml`
- `distill.yaml`
- `invocation_spectrum.yaml`
- `registry.yaml`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.