# Runtime Spine Build Record

## Status

The runtime spine build is complete for the Claude Code plugin-first bundle. This file records what shipped and what constraints remain, replacing the original scaffold-era build checklist.

## Delivered

1. Core state, registry, target resolution, Trace, Residue, Lever, transitions, artifacts, and provenance
2. Runtime-aware hook orchestration with pre/post pipeline validation
3. Marketplace-aware validation and family plugin packaging checks
4. Managed MCP definition loading plus on-demand endpoint probing and session reports
5. Approved experimental pipeline execution with explicit approval, evidence, and rollback requirements
6. Concurrent execution support for independent pipeline requests
7. HTML execution report rendering for plugin-facing review surfaces
8. End-to-end vertical slice execution and regression coverage

## Validation targets

Run these before calling the bundle complete:

```bash
python tools/validate_marketplace.py
python -m pytest tests -v --tb=short
python tools/probe_managed_mcp.py --timeout-seconds 0.5
python tools/run_vertical_slice.py
python tools/validate_bundle.py
```

## Product constraints

These are active operating constraints, not deferred implementation:

- managed MCP runtime support currently probes HTTP/HTTPS endpoints rather than hosting full bidirectional MCP sessions
- visualization is HTML report generation, not a persistent dashboard
- concurrency is only for independent pipeline requests with isolated state
- experimental pipelines require explicit approval payloads and remain non-default

## Source of truth

- `docs/implementation/taskboard_manifest.yaml`
- `docs/implementation/runtime_spine_scope.md`
