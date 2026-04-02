# AGENT GUIDE — shared/Trace/

Role note: Traveling selector controller. Smallest-sufficient intervention logic lives here.

## Build this directory exactly

Files that must exist in this directory:
- `checklist.yaml`
- `planner_loop.yaml`
- `rubric.yaml`
- `trigger_glossary.yaml`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Selector engine
- Planner loop

## Immediate child inventory

- `checklist.yaml`
- `planner_loop.yaml`
- `rubric.yaml`
- `trigger_glossary.yaml`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.