# AGENT GUIDE — entrypoints/

Purpose:
- This directory holds the build-facing family trees:
  - Forensics
  - Forge
  - Inquiry
  - Conduit

Build instruction:
- Each family must contain:
  - `selector.route.yaml`
  - `family_route_map.yaml`
- Forensics also contains `entry.skill.yaml`
- Each family's `pipelines/` subtree must match its route map inventory exactly.

Do not:
- place shared authorities here
- add live pipelines to selector scope unless they are also core in the family route map

## Build this directory exactly

Subdirectories that must exist:
- `Conduit/`
- `Forensics/`
- `Forge/`
- `Inquiry/`

## Build rules

- Keep filenames exact.
- Keep canonical ids exact.
- Preserve textual file contents exactly unless a later contract file explicitly says otherwise.
- Treat YAML files here as source-of-truth spec files, not examples.
- If this directory contains only subdirectories, create them anyway and place their own `AGENT.md` files.

## What consumes this directory

- Top-level build and validation flow

## Immediate child inventory

- `Conduit/`
- `Forensics/`
- `Forge/`
- `Inquiry/`

## Local no-brain instruction

Go to this directory. Build the exact child files and directories listed above. Preserve the naming scheme and contents. Do not reinterpret the role of this directory from neighboring directories.