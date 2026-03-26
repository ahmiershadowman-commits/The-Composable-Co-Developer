# Motif Layer Rationale

## Purpose

This document explains why motifs exist as a distinct layer in the marketplace runtime architecture and how they differ from primitives, operators, and evaluators.

## The Problem Motifs Solve

Large language models excel at pattern recognition but may not consistently attend to structurally important patterns without scaffolding. Traditional prompting approaches face a dilemma:

1. **Explicit rules** → Too rigid, become puppet-control strings
2. **No scaffolding** → Model may miss critical patterns inconsistently

Motifs provide a third way: **semantic conditioning** that influences attention without dictating actions.

## What Motifs Are

### Inference-Layer Semantic Conditioning

Motifs operate at the inference layer, shaping how the model interprets context rather than what actions it takes. They are:

- **Pattern detectors**: Recognize structural or semantic configurations
- **Attention modulators**: Increase salience of relevant features
- **Autonomy-preserving**: Suggest rather than command

### Hybrid Nature

Motifs are hybrid entities:

| Aspect | Motifs Are | Motifs Are Not |
|--------|------------|----------------|
| Triggering | Passive signals | Active triggers |
| Execution | No direct action | Don't invoke tools |
| Control | Influence attention | Don't bypass autonomy |
| Specificity | Domain-general patterns | Not task-specific rules |

## Architectural Position

### Relationship to Other Layers

```
Context → Motifs (pattern recognition)
           ↓
        Trace (intervention selection)
           ↓
    Primitives/Operators (action)
           ↓
      Evaluators (assessment)
```

**Key distinctions:**

- **Motifs vs Primitives**: Motifs detect; primitives act
- **Motifs vs Operators**: Motifs condition; operators transform
- **Motifs vs Evaluators**: Motifs signal; evaluators judge

### Why Motifs Aren't Triggers

Making motifs direct triggers would:

1. **Collapse layers**: Blend pattern recognition with action selection
2. **Reduce flexibility**: Same pattern may need different responses in different contexts
3. **Risk over-control**: Become hidden control logic rather than scaffolding

## The Four Core Motifs

### 1. Unfinished Proof (reasoning-gap)

**Purpose**: Detect incomplete reasoning chains

**Why it matters**: LLMs sometimes produce conclusions without adequate support. This motif increases attention on evidence gaps before commitment.

**Example detection**: "Therefore X" without preceding "because Y"

### 2. Watershed (decision-point)

**Purpose**: Mark high-stakes decision junctures

**Why it matters**: Some decisions are path-dependent and costly to reverse. This motif prompts explicit criteria articulation.

**Example detection**: Discussion of implementation start without decision criteria

### 3. Tension Point (conflict)

**Purpose**: Identify active disagreements

**Why it matters**: Unacknowledged tensions cause downstream failures. This motif prompts explicit conflict recognition.

**Example detection**: "Must be X" and "Must be not-X" in same context

### 4. Absence Signal (missingness)

**Purpose**: Surface conspicuously missing information

**Why it matters**: What's absent can be more important than what's present. This motif prompts pattern completion.

**Example detection**: Architecture doc without constraints section

## Design Principles

### 1. Preserve Autonomy

Motifs scaffold rather than control. They improve pattern recognition without dictating responses.

### 2. Stay at Inference Layer

Motifs influence how context is interpreted, not what actions are taken. Action selection remains with Trace and pipeline logic.

### 3. Be Domain-General

Core motifs apply across domains. Domain-specific patterns should be built from combinations of core motifs, not added as new motifs.

### 4. Remain Testable

Each motif must have:
- Clear detection signals
- Observable conditioning effect
- Empirical validation in worked traces

## When to Add New Motifs

Add a new motif ONLY when ALL are true:

1. **Pattern is structural**: Not domain-specific content
2. **Detection is reliable**: Can be identified consistently
3. **Conditioning helps**: Attention modulation improves outcomes
4. **Not redundant**: Existing motifs don't already cover it
5. **Empirically validated**: Worked traces show benefit

## Usage in Pipelines

Motifs are referenced in pipeline specs:

```yaml
smallest_sufficient_interventions:
  motifs:
    - unfinished-proof
    - watershed
```

**Guidelines:**

- Use 1-3 motifs per pipeline
- Combine motifs that address related patterns
- Don't over-condition (dilutes effect)
- Test empirically in worked traces

## Implementation Notes

### Motifs Are Not Hardcoded Rules

Motifs are semantic patterns loaded into context, not executable code. They work by:

1. Being present in the model's context window
2. Providing recognizable pattern descriptions
3. Suggesting related interventions without requiring them

### Motifs Don't Require Runtime Support

Unlike primitives or operators, motifs don't need runtime implementation. They are:

- Declarative YAML files
- Loaded as context by pipeline specs
- Always available when referenced

### Motifs Work with Trace

Trace may respond to motif signals by selecting appropriate interventions, but motifs don't trigger Trace directly. The relationship is:

```
Motif detected (in context) → Trace recognizes pattern → Trace selects intervention
```

## Summary

The motif layer exists because:

1. **LLMs need scaffolding** for consistent pattern recognition
2. **Explicit rules are too rigid** for flexible, autonomous behavior
3. **Semantic conditioning** provides a middle path
4. **Four core motifs** cover major pattern categories
5. **Architecture clarity** requires distinct layers

Motifs are the "attention lens" layer of the marketplace runtime—subtle but essential for reliable performance.
