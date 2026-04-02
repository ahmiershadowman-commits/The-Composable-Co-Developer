---
name: forensics
description: >
  This skill should be used when the user says "map this project", "establish ground truth",
  "the docs and code don't match", "I don't trust the current state", "things feel fragmented",
  "investigate this anomaly", "audit the documentation", "I need to understand what's actually
  here before making changes", or any time trust in the visible project surface has collapsed.
  Also triggers on "defragment", "reconcile docs", "isolate this anomaly", or "project drift".
metadata:
  version: "0.2.0"
  family: Forensics
---

# Forensics — Ground-Truth Establishment

Forensics is the entry point for any situation where the visible project surface cannot yet be trusted. Run Forensics before build or investigation work when documentation is suspect, state is fragmented, or contradictions exist.

## When to invoke

Invoke Forensics when any of these triggers are present:

- **trust_collapse**: The visible surface can no longer be treated as ground truth
- **suspect_documentation**: Docs may not reflect actual code or state
- **environment_mismatch**: Runtime behavior contradicts what sources say
- **project_drift_or_fragmentation**: Structure has diverged from canonical shape
- **anomaly_source_ambiguity**: Conflicting signals with unclear origin
- **high_consequence_state_mapping**: Stakes are high enough that acting on untrusted state is unacceptable

## Pipelines

Select the smallest sufficient pipeline:

| Pipeline | Alias | Use when |
|---|---|---|
| `project_mapping` | Survey | Project state needs mapping; canonical sources unclear; repository inventory needed |
| `defragmentation` | Gather | Entropy or fragmentation detected; project drift requires repair |
| `documentation_audit` | Reconcile | Docs disagree with code; multiple docs compete for truth |
| `anomaly_disambiguation` | Isolate | Suspicious signal needs source disambiguation; anomaly may be data artifact, process issue, or true misfit |

Default entry: `project_mapping`.

## Execution

Run via the portable pipeline runner. `${CLAUDE_PLUGIN_ROOT}` resolves to the plugin installation directory where this script lives.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Forensics <pipeline_id> "<scope description>"
```

Example:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Forensics project_mapping "auth module before refactoring"
```

Artifacts are written to `./runtime_output/` in your current working directory (the workspace), not inside the plugin. Read them from there.

## After execution

Read the artifacts from `./runtime_output/Forensics/<pipeline_id>/` and synthesize the findings. Key artifacts to surface:

- `trust_zone_map` — which areas can be trusted and which cannot
- `discrepancy_ledger` — identified conflicts between surfaces
- `route_recommendation` — what to do next (Forge, Inquiry, Conduit, or Defragmentation)
- `inventory_ledger` — what actually exists vs. what is claimed

## If execution fails

If the runtime script fails or is unavailable, execute the Forensics methodology directly:

1. **Scope**: State what is being examined and what is out of scope
2. **Inventory**: List what actually exists — files, dirs, configs, runtime components — by reading the filesystem with available tools (Read, Glob, Bash)
3. **Provenance**: Classify each source as observed, documented, or assumed
4. **Dependency graph**: Trace actual dependencies (imports, references, calls) rather than stated ones
5. **Discrepancy map**: Identify where documented state contradicts observed state
6. **Trust classification**: Assign trust levels (high / provisional / low / collapsed) per area
7. **Route recommendation**: State which family should handle the work next and why

Produce the same named artifacts as the runtime would, as structured notes or YAML in the conversation.

## Exit conditions

Do not declare Forensics complete until:

1. Scope is bounded
2. Observed state is inventoried sufficiently
3. Trust classification is explicit
4. Downstream route is justified
5. Carry-forward artifacts are written

## Routing after Forensics

Use the `route_recommendation` artifact to determine the next family:

- **Defragmentation** → entropy is the primary problem; structure needs repair before analysis
- **Forge** → state is grounded and build work can proceed
- **Inquiry** → state is grounded but interpretation or explanation is missing
- **Conduit** → communication or handoff work is now safe and primary

## References

- `references/artifacts.md` — Read this when you need the full field contract for an artifact you are producing or consuming (required fields, types, produced-by/consumed-by chain).
- `references/acceptance-matrix.md` — Read this when evaluating whether a pipeline has met its exit conditions before routing forward.

## Anti-patterns

**Do not proceed to Forge or Inquiry without completing Forensics when trust has collapsed.** Acting on untrusted state means the build or investigation is operating on a false substrate — errors compound silently and the output cannot be verified.

**Do not treat documentation as ground truth when the trigger is `suspect_documentation`.** Documentation is a claim surface, not an observation. When docs are suspect, they are evidence to be tested, not a source to be followed.

**Do not skip Defragmentation when entropy is actually the primary problem.** Routing directly to Forge when structure is fragmented produces changes that worsen fragmentation — each build adds to the disorder rather than resolving it.

**Do not declare Forensics complete without a trust classification.** A trust level without a routing justification, or a route without a trust level, means the downstream family is operating blind.
