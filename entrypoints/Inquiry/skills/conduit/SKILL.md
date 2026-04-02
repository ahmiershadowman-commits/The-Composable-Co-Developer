---
name: conduit
description: >
  This skill should be used when the user asks to "write documentation for", "create a handoff",
  "summarize this for someone else", "write a report on", "compress this into a transferable form",
  "write a paper", "draft a professional memo", "prepare this for a collaborator", or any task
  where the primary work is rendering accumulated structure into usable outward form. Also triggers
  on "clarify this for operators", "distill the key findings", "articulate this formally",
  "write this up for a non-technical audience", "handoff synthesis".
metadata:
  version: "0.2.0"
  family: Conduit
---

# Conduit — Communication and Synthesis

Conduit handles all output-rendering work: documentation, handoffs, professional writing, and scholarly synthesis. Use it when the primary task is to transfer structure to a reader, collaborator, operator, or future session — not to investigate or build. If source material conflicts with observed state or documentation truth is unclear, run Forensics first.

## When to invoke

- Operational or technical documentation is needed
- Accumulated material must be compressed without erasing load-bearing structure
- A formal, argumentative, or scholarly output is needed
- A professional or operational audience needs clarity with narrative and recommendations

Do not invoke Conduit when `documentation_truth_unclear` or `source_material_conflicts_with_observed_state` — reroute to Forensics first. Do not let Conduit render unsupported claims without rerouting to Inquiry.

## Pipelines

Select the smallest sufficient pipeline:

| Pipeline | Alias | Use when |
|---|---|---|
| `documentation` | Clarify | Operational or technical documentation is needed |
| `handoff_synthesis` | Distill | Accumulated material must be compressed without erasing load-bearing structure |
| `scholarly_writing` | Articulate | Formal, argumentative, or scholarly output is needed |
| `professional_writing` | Convey | Professional or operational audience needs clarity; narrative and recommendations but not scholarly rigor |

Default entry: `documentation`.

## Execution

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Conduit <pipeline_id> "<content description>"
```

Example:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Conduit handoff_synthesis "compress session findings for next agent"
```

Artifacts are written to `./runtime_output/Conduit/<pipeline_id>/` in your current working directory.

## After execution

Read the artifacts from `./runtime_output/Conduit/<pipeline_id>/` and deliver the output to the user. Key artifacts:

- `draft_document` / `handoff_document` / `final_document` — the primary written output
- `support_note` / `claim_hierarchy` — check this before delivering; flag unsupported claims
- `unresolveds_and_risks` — must transfer with any handoff
- `route_recommendation` — if gaps were found requiring Inquiry or Forensics

## If execution fails

Execute the Conduit methodology directly:

1. **Scope the audience**: State who is reading this and what decision or action it supports
2. **Gather source material**: Identify what accumulated content exists to render (Read artifacts, conversation history, docs)
3. **Map load-bearing structure**: Identify what must not be compressed away
4. **Draft**: Write the output, rendering structure into appropriate form for the audience
5. **Check support**: Flag any claim that lacks adequate backing before delivering
6. **Surface unresolveds**: Explicitly list open questions, risks, and incomplete work in the output

Produce the same named artifacts as structured notes.

## Exit conditions

Do not declare Conduit work complete until:

1. The output audience and purpose are explicit
2. Load-bearing structure from source material is preserved (not compressed away)
3. Unsupported claims are flagged, not silently included
4. Output artifact is written to `runtime_output/`

## Pipeline feedback loops

- `documentation` → `handoff_synthesis` when branch accumulation is high
- `scholarly_writing` → Inquiry when support is weak or concepts are underbound
- `professional_writing` → Inquiry when underlying claims or support are weak
- `professional_writing` → `scholarly_writing` when formal argument is required
- Any Conduit pipeline → Forensics when documentation truth becomes unclear mid-render

## References

- `references/artifacts.md` — Full artifact contracts for all Conduit pipelines
- `references/acceptance-matrix.md` — Exit criteria per pipeline

## Anti-patterns

Do not let Conduit render unsupported claims — reroute to Inquiry to fill the gap first. Do not use `scholarly_writing` for operational docs (use `documentation`). Do not use `handoff_synthesis` as a first step when source material hasn't been analyzed yet.
