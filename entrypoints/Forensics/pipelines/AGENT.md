# AGENT GUIDE — entrypoints/Forensics/pipelines/

## Build this directory exactly

Subdirectories that must exist:
- `anomaly_disambiguation/`
- `defragmentation/`
- `documentation_audit/`
- `introspection_audit/`
- `label_shift_correction/`
- `project_mapping/`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Family selectors
- Family route maps
- Pipeline loaders
- Runtime route resolution

## Immediate child inventory

- `anomaly_disambiguation/`
- `defragmentation/`
- `documentation_audit/`
- `introspection_audit/`
- `label_shift_correction/`
- `project_mapping/`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.