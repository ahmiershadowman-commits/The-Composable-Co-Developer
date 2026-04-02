# AGENT GUIDE — runtime/schemas/

Role note: Canonical grammar/spec contracts.

## Build this directory exactly

Files that must exist in this directory:
- `pipeline.yaml`
- `selector.py`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Tests
- Loaders
- Runtime validators

## Immediate child inventory

- `pipeline.yaml`
- `selector.py`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.