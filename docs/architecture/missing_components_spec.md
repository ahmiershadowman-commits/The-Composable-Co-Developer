# Missing Components Specification

Last updated: 2026-04-02

## Current status

This document used to track gaps from the early marketplace build pass. The plugin-first
bundle has now closed the previously listed missing items for:

- family plugin manifests and marketplace packaging
- skills, commands, agents, and portable runners
- shared motifs and operators
- runtime execution semantics docs
- worked trace expansion
- Inquiry `data_analysis` executor wiring
- hook/interface contract documentation
- operator README coverage
- unresolveds ledger schema
- machine-readable taskboard manifest
- managed MCP probing
- HTML runtime report rendering
- concurrent execution for independent pipeline requests
- approved experimental pipeline execution paths

## No current blocking gaps

There are no known missing components that block the Claude Code marketplace bundle or the
core runtime spine for production use of the core families.

## Current operating constraints

The following are active product constraints, not deferred implementation work:

1. Managed MCP support currently probes HTTP/HTTPS endpoints and validates credentials. Full bidirectional MCP hosting is optional future scope.
2. Visualization is delivered as generated HTML reports rather than a persistent dashboard.
3. Concurrency is limited to independent requests with isolated state.
4. Experimental pipelines are available only when explicit empirical approval is supplied.

## Source of truth

Use `docs/implementation/taskboard_manifest.yaml` for machine-readable component status and
`docs/implementation/runtime_spine_scope.md` for scope boundaries.
