# Build Plan by Branch Priority

This file orders the build branches by importance and dependency.

## Priority order

### Priority 0 — Runtime spine
Build first.
Nothing else should be treated as executable until the spine exists.

File:
- `docs/implementation/runtime_spine_build_plan.md`

### Priority 1 — Shared authorities
Build next because every family depends on them:
- Trace
- Lever
- Residue
- primitives
- operators
- feedback loop interpreter support

File:
- `docs/implementation/shared_authorities_build_plan.md`

### Priority 2 — Forensics
Build first family because it establishes trust and route safety for all others.

File:
- `docs/implementation/forensics_build_plan.md`

### Priority 3 — Forge
Build second family because it is the first real change/build path and depends on Forensics.

File:
- `docs/implementation/forge_build_plan.md`

### Priority 4 — Inquiry
Build third because it depends on stable truth surfaces and sometimes feeds Conduit.

File:
- `docs/implementation/inquiry_build_plan.md`

### Priority 5 — Conduit
Build fourth because it often consumes outputs from Forensics, Forge, and Inquiry.

File:
- `docs/implementation/conduit_build_plan.md`

## Sequencing rule

- build the spine serially
- build shared authorities before family-specific executors
- validate Forensics before trusting Forge
- validate Forge before broadening Inquiry and Conduit
- keep experimental pipelines parked until core family execution is stable
