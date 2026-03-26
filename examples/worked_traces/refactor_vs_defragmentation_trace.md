# Refactor vs Defragmentation Trace

Demonstrates the decision boundary between Refactor (Forge) and Defragmentation (Forensics).

## Scenario

Codebase has become hard to work with. Should we refactor or defragment?

## Decision Boundary

| Signal | Refactor (Forge) | Defragmentation (Forensics) |
|--------|------------------|----------------------------|
| Trust | Code structure is trusted | Structure is uncertain |
| Problem | Code quality issues | Coherence/fragmentation issues |
| Goal | Improve design | Restore coherent structure |
| Entry | Safe to build | Need ground truth first |

---

## Scenario A: Refactor is Correct

### Initial State

```yaml
trust_assessment:
  trust_level: "high"
  canonical_sources_identified: true
  entropy_level: "low"

problem: "Code works but is hard to extend"
```

### Trace Decision

```yaml
trace_decision:
  action: "continue"
  target: "family:Forge"
  pipeline: "refactor"
  reason: "Structure trusted - quality improvement needed"
  intervention_band: 2
```

### Forge/refactor Execution

```yaml
pipeline: "Forge/refactor"

phases:
  - map: "Current code structure mapped"
  - invariants: "Behavior invariants identified"
  - plan: "Refactor plan created"
  - execute: "Refactoring performed"
  - validate: "Behavior preserved"
  - recommend: "Next steps"

artifacts:
  - current_shape_map
  - invariants_ledger
  - refactor_plan
  - refactored_artifact
  - behavior_validation
```

---

## Scenario B: Defragmentation is Correct

### Initial State

```yaml
trust_assessment:
  trust_level: "low"
  canonical_sources_identified: false
  entropy_level: "high"

problem: "Multiple conflicting module structures"
```

### Trace Decision

```yaml
trace_decision:
  action: "cross_family_reroute"
  target: "family:Forensics"
  pipeline: "defragmentation"
  reason: "Structure uncertain - coherence needed before refactor"
  intervention_band: 8
```

### Forensics/defragmentation Execution

```yaml
pipeline: "Forensics/defragmentation"

phases:
  - inspect_state: "Fragmentation is severe"
  - classify_entropy: "High entropy"
  - choose_method: "Consolidate method"
  - execute_method: "Canonical structure identified"
  - normalize: "Metadata aligned"
  - verify: "Coherence restored"
  - reroute: "Ready for Forge"

artifacts:
  - canonical_structure_map
  - residue_disposition_ledger
  - metadata_normalization_record
  - trust_reassessment_note
  - route_recommendation -> Forge/refactor
```

### Then Forge/refactor

```yaml
# After defragmentation establishes canonical structure
pipeline: "Forge/refactor"
# Now safe to refactor
```

---

## Decision Flow

```
User: "Codebase is hard to work with"
  |
  v
Trace evaluates trust + entropy
  |
  +-----------------------------+
  | Trust HIGH + Entropy LOW    |
  | -> Forge/refactor           |
  +-----------------------------+
  | Trust LOW + Entropy HIGH    |
  | -> Forensics/defragmentation|
  | -> Then Forge/refactor      |
  +-----------------------------+
```

---

## Key Distinction

**Refactor** assumes the structure is known and trusted, but quality is poor.

**Defragmentation** assumes the structure itself is uncertain or conflicted.

---

## Assertions

1. Trust determines route: High trust -> Forge, Low trust -> Forensics
2. Defragmentation restores coherence: Only after can refactor proceed
3. Never skip Defragmentation: When entropy is primary problem
4. Trace selects correctly: Based on trust/entropy assessment
