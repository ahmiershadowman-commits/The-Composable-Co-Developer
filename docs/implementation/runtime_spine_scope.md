# Runtime Spine Scope

## What the spine is

The runtime spine is the adaptive kernel underneath the Claude Code marketplace bundle. It now:

- loads and indexes the marketplace spec bundle
- validates schema and inventory consistency
- resolves canonical targets to typed objects
- executes Trace as the traveling metacognitive controller
- dispatches Residue lenses for suspicious-surface investigation
- escalates to Lever for bounded evaluation
- transitions legally across phase, pipeline, and family boundaries
- executes pre/post pipeline python hooks through the runtime dispatcher
- loads managed MCP definitions from `managed-mcp.json`
- probes managed MCP endpoints on demand and records session health
- supports concurrent execution of independent pipeline requests
- renders HTML execution reports for plugin-facing review surfaces
- executes approved experimental pipelines with explicit empirical approval records
- persists checkpoints and execution logs
- emits artifacts and provenance records
- runs the end-to-end vertical slice

## What the spine is not

The spine is not:

- a full desktop GUI application
- an automatic promoter of experimental pipelines without approval
- a replacement for Claude Code marketplace packaging

## Current boundaries

The spine is complete for the plugin-first bundle. Current limits are product decisions rather than deferred implementation:

1. Managed MCP probing currently targets HTTP/HTTPS endpoints; full bidirectional MCP protocol hosting can be added if product requirements demand it.
2. Visualization is HTML report generation rather than a persistent live dashboard.
3. Concurrency is limited to independent pipeline requests; shared-state mutation still runs through the normal sequential dispatcher.
4. Experimental pipelines require explicit approval payloads with evidence and rollback plans.

## Spine success criteria

The spine is complete when:

1. Registry can load and index the bundle
2. Every runtime target resolves to a typed object or structured error
3. Trace can choose a smallest-sufficient action
4. Residue can propose structured interventions
5. Lever can return structured evaluation results
6. Hooks can validate and review pipeline execution
7. Managed MCP definitions can be loaded, validated, and probed
8. Checkpoints and provenance can be written to disk
9. Execution reports can be rendered for plugin review surfaces
10. Independent pipeline requests can run concurrently
11. Experimental pipelines can run only with explicit empirical approval
12. Vertical slice runs: Forensics -> Defragmentation -> Forensics -> Forge

## Future enhancements

If product scope expands beyond the current CLI-first bundle:

- add full bidirectional MCP protocol session hosting
- add a persistent live dashboard on top of the HTML reports
- add coordinated shared-state concurrency controls
- extend experimental approval policy to external governance systems
