---
name: inquiry
description: >
  This skill should be used when the user asks "why does this happen", "explain how this works",
  "investigate this", "what's causing this", "analyze this data", "generate hypotheses about",
  "formalize this concept", "prove this", "research the options for", or any task where the
  primary work is understanding, explanation, evidence collection, or formal analysis rather
  than artifact change. Also triggers on "synthesize the evidence", "what are the possible
  explanations", "derive this", "model this data", "bind these concepts formally".
metadata:
  version: "0.2.0"
  family: Inquiry
---

# Inquiry — Investigation and Explanation

Inquiry handles all understanding, analysis, and formal investigation work. Use it when the task is to explain, investigate, reason about, or formalize — not to build or change artifacts. If source truth is suspect or anomaly origin is unclear, run Forensics first.

## When to invoke

- Evidence collection, comparison, or synthesis is needed
- An explanation or hypothesis is required for an anomaly or open causal slot
- Data needs inspection, validation, or modeling
- Concepts or relationships need explicit formal structure
- Proof, derivation, counterexample, or mathematical rigor is the primary goal

Do not invoke Inquiry when `source_truth_suspect`, `anomaly_source_ambiguous`, or `documentation_or_state_claims_untrusted` — reroute to Forensics first.

## Pipelines

Select the smallest sufficient pipeline:

| Pipeline | Alias | Use when |
|---|---|---|
| `research` | Seek | Evidence collection, comparison, or synthesis is needed |
| `hypothesis_generation` | Venture | Explanatory frames are needed; anomaly or open causal slot exists |
| `data_analysis` | Read | Data needs inspection, validation, or modeling |
| `formalization` | Bind | Concepts or relations need explicit structure |
| `mathematics` | Resolve | Proof, derivation, counterexample, or rigor is primary |

Experimental (not available): `prompt_order_optimization`, `human_hint_integration`.

Default entry: `research`.

## Execution

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Inquiry <pipeline_id> "<research question>"
```

Example:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Inquiry research "what are the options for replacing the session middleware"
```

Artifacts are written to `./runtime_output/Inquiry/<pipeline_id>/` in your current working directory.

## After execution

Read the artifacts from `./runtime_output/Inquiry/<pipeline_id>/` and synthesize findings. Key artifacts:

- `question_frame` — bounded statement of what is being investigated
- `source_ledger` — sources consulted with trust classification
- `synthesis_note` / `hypothesis_set` — what the evidence converges on
- `route_recommendation` — next step if follow-on work is needed

## If execution fails

Execute the Inquiry methodology directly:

1. **Frame the question**: State exactly what is being investigated and what would count as a satisfactory answer
2. **Collect evidence**: Use available tools to gather relevant sources (Read, Grep, Glob, Bash, WebSearch)
3. **Compare**: Map competing evidence, sources, or explanations side by side
4. **Synthesize**: State what the evidence supports and where gaps remain
5. **Route**: If explanation is open → hypothesis_generation; if formal structure needed → formalization

Produce the same named artifacts as structured notes.

## Exit conditions

Do not declare Inquiry work complete until:

1. The question or investigation scope is bounded
2. Evidence or analysis is sufficient to support the output claims
3. Artifacts are written to `runtime_output/`
4. Unresolved threads are explicitly noted, not silently dropped

## Pipeline feedback loops

- `research` → `hypothesis_generation` when evidence exists but explanation is open
- `hypothesis_generation` → `research` when evidence is insufficient for hypothesis selection
- `formalization` → `mathematics` when the object language is stable enough for rigorous work
- `mathematics` → `formalization` when underspecification or symbol instability is detected
- Any Inquiry pipeline → Forensics when source truth becomes suspect mid-investigation

## References

- `references/artifacts.md` — Read this when you need the full field contract for an artifact you are producing or consuming.
- `references/acceptance-matrix.md` — Read this when evaluating whether a pipeline has met its exit conditions before routing forward.

## Anti-patterns

**Do not let Inquiry continue on untrusted state surfaces.** Investigation on untrusted sources produces confident-looking outputs built on unreliable inputs — the synthesis note and hypothesis set inherit the trust deficit of their sources. Reroute to Forensics before continuing.

**Do not use `hypothesis_generation` as a substitute for `research` when evidence exists but hasn't been collected.** Generating hypotheses without first gathering evidence means the candidates are unconstrained by what is actually true — you get plausible-sounding explanations rather than evidence-discriminated ones. Run `research` first to constrain the hypothesis space.

**Do not declare synthesis complete when gaps remain unexplained.** Unresolved threads dropped silently become invisible assumptions in downstream work. Name them explicitly in the `support_and_gap_map` before routing forward.

**Do not promote experimental pipelines (`prompt_order_optimization`, `human_hint_integration`) to default use.** These pipelines are not validated for general use — their failure modes are not characterized and their outputs should not be treated as reliable.
