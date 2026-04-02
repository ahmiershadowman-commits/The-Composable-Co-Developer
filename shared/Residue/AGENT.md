# AGENT GUIDE — shared/Residue/

Role note: Suspicious-surface lens library. Use it to notice and investigate before over-rerouting.

## Build this directory exactly

Files that must exist in this directory:
- `absence.yaml`
- `burden.yaml`
- `edge.yaml`
- `misfit.yaml`
- `offset.yaml`
- `registry.yaml`
- `signal.yaml`
- `tension.yaml`
- `trigger_map.yaml`
- `warp.yaml`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Trace when suspicious-surface oddity is detected
- Lever when a lens escalates to evaluation

## Immediate child inventory

- `absence.yaml`
- `burden.yaml`
- `edge.yaml`
- `misfit.yaml`
- `offset.yaml`
- `registry.yaml`
- `signal.yaml`
- `tension.yaml`
- `trigger_map.yaml`
- `warp.yaml`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.