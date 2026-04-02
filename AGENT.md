# AGENT GUIDE — ./

Purpose:
- This is the repository root.
- It holds the global contract, inventory, top-level docs, runtime, shared layers,
  entrypoint families, examples, tools, and tests.

Build instruction:
- Create every listed top-level directory exactly as named.
- Build textual files exactly as named.
- Preserve the naming distinction between:
  - canonical ids
  - frame aliases
  - primitives
  - operators
  - evaluators
  - families
  - authorities

Do not:
- rename top-level families
- add alternate top-level runtimes
- move shared authorities into family trees
- flatten family boundaries

## Build this directory exactly

Subdirectories that must exist:
- `docs/`
- `entrypoints/`
- `examples/`
- `runtime/`
- `shared/`
- `tests/`
- `tools/`

Files that must exist in this directory:
- `README.md`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Top-level build and validation flow

## Immediate child inventory

- `docs/`
- `entrypoints/`
- `examples/`
- `runtime/`
- `shared/`
- `tests/`
- `tools/`
- `README.md`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.