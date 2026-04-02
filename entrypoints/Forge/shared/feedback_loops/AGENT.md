# AGENT GUIDE — shared/feedback_loops/

Role note: Loop topology files. Must stay consistent with route maps and selectors.

## Build this directory exactly

Files that must exist in this directory:
- `README.md`
- `conduit.yaml`
- `forensics.yaml`
- `forge.yaml`
- `global.yaml`
- `inquiry.yaml`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Top-level build and validation flow

## Immediate child inventory

- `README.md`
- `conduit.yaml`
- `forensics.yaml`
- `forge.yaml`
- `global.yaml`
- `inquiry.yaml`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.