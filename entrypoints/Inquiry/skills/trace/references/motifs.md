# Motifs

Motifs are inference-layer semantic conditioning — not rules, not triggers. They increase attention on specific structural patterns without dictating responses. They are the lightest intervention in the stack, applied before primitives.

Motifs detect; they don't act. Trace may respond to motif signals by selecting interventions, but motifs don't bypass reasoning autonomy.

## Core motifs

### unfinished-proof (reasoning-gap)
**Detects**: Incomplete reasoning chains — conclusions without adequate support
**Watch for**: "Therefore X" without "because Y"; commitment under insufficient evidence
**Effect**: Increases attention on evidence gaps before commitment is made
**Use in**: Forensics (primary bias), Inquiry, any pipeline where claims are being made

### watershed (decision-point)
**Detects**: High-stakes decision junctures — path-dependent choices that are costly to reverse
**Watch for**: Implementation starting without explicit decision criteria; irreversible actions without prior commitment checks
**Effect**: Prompts explicit criteria articulation before proceeding
**Use in**: Forensics (secondary bias), Forge, any pipeline approaching commitment

### tension-point (conflict)
**Detects**: Active disagreements between surfaces, sources, or claims
**Watch for**: "Must be X" and "Must be not-X" in same context; competing sources with no resolution
**Effect**: Prompts explicit conflict recognition rather than silent smoothing
**Use in**: Inquiry, Forensics/documentation_audit, any investigation pipeline

### absence-signal (missingness)
**Detects**: Conspicuously missing information — what's absent may matter more than what's present
**Watch for**: Architecture doc without constraints section; explanation without failure cases; audit without gaps noted
**Effect**: Prompts pattern completion before proceeding
**Use in**: Forensics, Conduit, any pipeline that could render a complete-seeming but incomplete output

## Usage rules

- Load 1-3 motifs per pipeline; don't over-condition
- Motifs are listed in pipeline specs under `smallest_sufficient_interventions.motifs`
- They are declarative YAML loaded as context — no runtime implementation needed
- Never use motifs as direct triggers or as substitutes for evaluators
- Motifs that feel uncomfortable without clear reason are often catching something real — take them seriously
