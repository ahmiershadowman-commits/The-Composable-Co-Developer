# The Composable Co-Developer Marketplace Runtime

## Project Overview

This repository contains a **normalized marketplace runtime specification bundle** for a composable AI co-developer system. It defines an architecture where multiple specialized "families" of capabilities work together through well-defined pipelines, shared authorities, and routing mechanisms.

The system is designed as a **handoff-safe build contract** - another technical agent should be able to build the system from this package without inventing architecture or reinterpreting routing semantics.

### Core Architecture

The system is built around **7 locked macro roles**:

| Role | Purpose |
|------|---------|
| **Forensics** | Deep ground-truth entrypoint - establishes truth when the surface cannot be trusted |
| **Forge** | Build/change family - shapes, modifies, validates artifacts when trustworthy state exists |
| **Inquiry** | Question/evidence/explanation/formal investigation family |
| **Conduit** | Documentation/writing/synthesis/handoff family |
| **Trace** | Traveling metacognitive controller - applies smallest sufficient intervention |
| **Lever** | Evaluator/escalation/commitment authority - owns pivots, commitments, reopen rules |
| **Residue** | Suspicious-surface lens library - provides investigative lenses |

### Key Design Principles

1. **Forensics establishes truth** - the only deep ground-truth entrypoint
2. **Defragmentation restores coherence** - owned by Forensics
3. **Trace supervises** with the smallest sufficient intervention before heavier escalation
4. **Lever escalates, evaluates, commits, and reopens**
5. **Residue supplies suspicious-surface lenses** - not a pipeline family
6. **Pipelines are end-to-end micro-methodologies** with entry conditions, phase order, pivot conditions, exit conditions, and artifacts

## Directory Structure

```
The Composable Co-Developer/
├── docs/                      # Architecture docs, audits, validation reports
│   ├── architecture/          # Bundle status, locked contract, family packets
│   ├── audits/                # Experimental pipeline audits
│   ├── implementation/        # Build plans for each family
│   ├── research/              # Dependency graphs
│   └── validation/            # Validation reports
├── entrypoints/               # Family entry points
│   ├── Conduit/               # Documentation/handoff family
│   ├── Forensics/             # Ground-truth family (has entry.skill.yaml)
│   ├── Forge/                 # Build/change family
│   └── Inquiry/               # Investigation family
├── examples/                  # Worked traces demonstrating system behavior
│   └── worked_traces/
├── runtime/                   # Core runtime specifications
│   ├── methodology/           # Target grammar, trust classes
│   └── schemas/               # Pipeline schema, selector logic
├── shared/                    # Shared authorities and components
│   ├── Lever/                 # Commitment, escalation, evaluator rules
│   ├── Residue/               # Investigative lens definitions
│   ├── Trace/                 # Rubric, checklist, planner, trigger glossary
│   ├── feedback_loops/        # Cross-family and intra-family feedback
│   ├── operators/             # Reusable operator classes
│   └── primitives/            # Smallest reusable interventions
│       ├── metacognitive/     # center, open, trim, shift, hold, release, locate
│       └── reasoning/         # reread, weave, separate, bind, press
├── tests/                     # Structural validation tests
│   ├── routing/               # Route map and selector tests
│   ├── schemas/               # Pipeline and grammar tests
│   └── worked_examples/       # Worked trace assertions
├── tools/                     # Validation utilities
├── README.md                  # Bundle overview
├── BUILD_CONTRACT.md          # Build contract for technical agents
├── INVENTORY_MANIFEST.md      # Complete file/directory inventory
└── AGENT.md                   # Directory build guide
```

## Building and Running

### Validation

The bundle includes structural validation tests (not runtime execution tests):

```bash
python tools/validate_bundle.py
```

This runs:
- Pipeline schema conformance checks
- Canonical target grammar and target resolution
- Family route map inventory consistency
- Selector scope consistency
- Worked trace presence and basic assertion checks

### Build Order

When implementing this system, build in this order:

1. Runtime grammar and schemas (`runtime/schemas/pipeline.yaml`, `runtime/methodology/target_grammar.yaml`)
2. Shared authorities (Trace, Lever, Residue)
3. Shared primitives
4. Shared operators
5. Family route maps
6. Selectors
7. Forensics family
8. Forge family
9. Inquiry family
10. Conduit family
11. Feedback loops
12. Worked examples
13. Tests and validators

### Acceptance Gates

A builder should not call the system "done" until all gates pass:

| Gate | Description |
|------|-------------|
| **Grammar** | Canonical pipeline grammar, target grammar, route grammar all present and consistent |
| **Inventory** | Every listed file/directory exists; no ghost pipelines in selectors or route maps |
| **Family Coherence** | Route maps match live pipeline inventory; selectors only scope core pipelines |
| **Target Resolution** | Every selector, route map, loop file, and pivot target resolves |
| **Semantic Architecture** | Forensics, Defragmentation, Trace, Lever, Residue retain exact roles |
| **Validation** | All tests pass; worked traces remain valid |

## Development Conventions

### Canonical Target Grammar

All runtime targets must use one of these forms:

```yaml
- primitive:<name>
- operator:<name>
- evaluator:<name>
- method:<name>
- pipeline:<Family>/<pipeline_id>
- family:<Family>
- authority:<Trace|Lever|Residue>
- forensics_reset
```

**Frame aliases are frontmatter only** - never use them as runtime identifiers.

### Pipeline Schema

All pipelines must conform to `runtime/schemas/pipeline.yaml` with these required fields:

- `id` - plain snake_case canonical pipeline identifier
- `family` - one of Forensics, Forge, Inquiry, Conduit
- `kind` - must be `end_to_end_pipeline`
- `frame_alias` - gentle mode-bias alias for human/model-facing frontmatter
- `status` - `core` | `experimental` | `incubating`
- `entry_conditions` - conditions under which this pipeline is appropriate
- `shared_authorities` - trace, lever, residue references
- `phase_order` - ordered list of phase ids
- `phase_contracts` - per-phase goal/output contracts
- `smallest_sufficient_interventions` - motifs, primitives, operators, evaluators
- `pivot_conditions` - trigger-to-action map
- `exit_conditions` - truth, artifact, provenance, and residue requirements
- `artifacts` - primary deliverables and supporting metadata

### Core vs Experimental Pipelines

**Core families and pipelines:**

| Family | Pipelines |
|--------|-----------|
| **Forensics** | `project_mapping`, `defragmentation`, `documentation_audit`, `anomaly_disambiguation` |
| **Forge** | `development`, `coding`, `testing`, `refactor` |
| **Inquiry** | `research`, `hypothesis_generation`, `data_analysis`, `formalization`, `mathematics` |
| **Conduit** | `documentation`, `scholarly_writing`, `professional_writing`, `handoff_synthesis` |

**Experimental pipelines** (must remain explicitly marked):

| Family | Experimental Pipelines |
|--------|------------------------|
| **Forensics** | `label_shift_correction`, `introspection_audit` |
| **Inquiry** | `prompt_order_optimization`, `human_hint_integration` |

### Anti-Patterns to Avoid

Do **not**:
- Flatten families into one plugin bucket
- Treat docs as truth before Forensics when trust is uncertain
- Collapse primitives/operators/evaluators into a single action class
- Use aliases as canonical ids
- Turn Residue into a generic "analysis" family
- Let Forge continue when truth has collapsed
- Let Conduit render unsupported claims without rerouting
- Let Inquiry continue on untrusted state surfaces
- Skip Defragmentation when entropy is actually primary

## Key Files

| File | Purpose |
|------|---------|
| `runtime/schemas/pipeline.yaml` | Canonical schema for all pipeline specifications |
| `runtime/methodology/target_grammar.yaml` | Canonical target grammar for selectors and routing |
| `shared/Trace/rubric.yaml` | Persistent low-cost supervision rubric |
| `shared/Residue/registry.yaml` | Investigative lens registry (misfit, absence, tension, warp, etc.) |
| `shared/primitives/registry.yaml` | Shared primitive inventory (metacognitive and reasoning) |
| `shared/operators/registry.yaml` | Reusable operator classes with intervention bands |
| `entrypoints/Forensics/entry.skill.yaml` | Forensics entry point skill definition |
| `entrypoints/*/family_route_map.yaml` | Authoritative family routing configuration |
| `entrypoints/*/selector.route.yaml` | Selector scope definitions |
| `shared/feedback_loops/*.yaml` | Cross-family and intra-family feedback structure |

## Worked Example

The bundle includes a complete worked trace at `examples/worked_traces/forensics_defragmentation_forge_trace.md` demonstrating:

1. Trust collapse → enter **Forensics/project_mapping**
2. Entropy detected → route to **Forensics/defragmentation**
3. Coherence restored → recheck in **Forensics/project_mapping**
4. Safe build state → route to **Forge/development**
5. Bounded change → **Forge/coding**
6. Validation → **Forge/testing**

This trace preserves the load-bearing distinction: Forensics establishes truth, Defragmentation restores coherence, Trace supervises interventions, and Forge resumes only after the surface becomes trustworthy.
