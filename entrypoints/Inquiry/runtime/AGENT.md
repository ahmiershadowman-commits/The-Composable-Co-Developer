# AGENT GUIDE — runtime/

Purpose:
- Runtime grammar and schema layer.
- This directory defines how the rest of the repository is interpreted.

Build instruction:
- Keep runtime files literal and infrastructure-like.
- Do not rename these files into more poetic variants.
- These files should be consumed by implementation code and tests.

Do not:
- move family-specific semantics into runtime
- encode aliases as canonical runtime ids

## Build this directory exactly

Subdirectories that must exist:
- `methodology/`
- `schemas/`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Top-level build and validation flow

## Immediate child inventory

- `methodology/`
- `schemas/`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.