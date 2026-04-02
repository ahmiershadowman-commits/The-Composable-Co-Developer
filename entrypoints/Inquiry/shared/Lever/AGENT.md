# AGENT GUIDE — shared/Lever/

Role note: Evaluator/pivot/commitment authority. Escalation and adjudication live here.

## Build this directory exactly

Files that must exist in this directory:
- `commitment_rules.yaml`
- `escalation_rules.yaml`
- `evaluator_registry.yaml`
- `reroute_rules.yaml`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Evaluator invocation layer
- Escalation and commitment logic

## Immediate child inventory

- `commitment_rules.yaml`
- `escalation_rules.yaml`
- `evaluator_registry.yaml`
- `reroute_rules.yaml`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.