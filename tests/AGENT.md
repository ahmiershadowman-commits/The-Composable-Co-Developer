# AGENT GUIDE — tests/

Purpose:
- Mechanical validation layer for the spec bundle.

Build instruction:
- Keep tests structural and contract-oriented.
- These tests are not the runtime; they are checks on the spec grammar and inventory.

Do not:
- silently disable failing tests instead of fixing the underlying spec/build mismatch

## Build this directory exactly

Subdirectories that must exist:
- `routing/`
- `schemas/`
- `worked_examples/`

Files that must exist in this directory:
- `README.md`
- `_util.py`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Top-level build and validation flow

## Immediate child inventory

- `routing/`
- `schemas/`
- `worked_examples/`
- `README.md`
- `_util.py`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.