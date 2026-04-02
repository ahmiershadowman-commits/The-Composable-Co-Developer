# AGENT GUIDE — shared/

Purpose:
- Shared cross-family resources.
- Houses Trace, Lever, Residue, primitives, operators, and feedback loops.

Build instruction:
- Keep these as shared, not nested under any family.
- Any implementation should load these once and reuse them across families.

Do not:
- duplicate these resources into family-specific versions unless a later spec explicitly introduces local overrides

## Build this directory exactly

Subdirectories that must exist:
- `Lever/`
- `Residue/`
- `Trace/`
- `feedback_loops/`
- `operators/`
- `primitives/`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Top-level build and validation flow

## Immediate child inventory

- `Lever/`
- `Residue/`
- `Trace/`
- `feedback_loops/`
- `operators/`
- `primitives/`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.