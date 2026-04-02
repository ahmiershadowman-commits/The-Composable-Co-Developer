# AGENT GUIDE — tests/routing/

Role note: Tests for route map and selector consistency.

## Build this directory exactly

Files that must exist in this directory:
- `test_family_route_maps.py`
- `test_selector_scopes.py`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Validation runner
- CI or local verification

## Immediate child inventory

- `test_family_route_maps.py`
- `test_selector_scopes.py`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.