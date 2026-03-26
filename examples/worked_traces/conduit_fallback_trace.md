# Conduit Fallback Trace - Worked Example

Demonstrates Conduit execution when trust collapses mid-pipeline, requiring Defragmentation.

## Scenario

Team asks for handoff documentation, but project state is too fragmented for reliable synthesis.

## Execution Flow

```
User Request → Trace → Conduit/handoff_synthesis → Trust Collapse → Forensics/defragmentation → Conduit/handoff_synthesis (retry)
```

## Step-by-Step

### Step 1: Initial Request

```yaml
user_prompt: "Create a handoff document for the new team taking over"
```

### Step 2: Trace Evaluation (Initial)

```yaml
trace_decision:
  action: "continue"
  target: "family:Conduit"
  reason: "Handoff synthesis requested"
  intervention_band: 1
```

### Step 3: Conduit/handoff_synthesis (Attempt 1)

```yaml
pipeline: "Conduit/handoff_synthesis"

phase_failure:
  phase: "sources"
  error: "Cannot reconcile conflicting documentation sources"
  trust_collapse: true
```

### Step 4: Trace Evaluation (Trust Collapse)

```yaml
trace_decision:
  action: "cross_family_reroute"
  target: "family:Forensics"
  reason: "Trust collapsed - documentation conflicts detected"
  intervention_band: 8
  
suspicious_surface:
  type: "tension"
  description: "API docs contradict README"
```

### Step 5: Residue Consultation

```yaml
residue_lens: "tension"
interpretation: "Active conflict between documentation sources"
recommendation: "Defragmentation before synthesis"
```

### Step 6: Forensics/defragmentation

```yaml
pipeline: "Forensics/defragmentation"

phases:
  - inspect_state: "Document fragmentation is severe"
  - classify_entropy: "High entropy - multiple canonical candidates"
  - choose_method: "Consolidate method selected"
  - execute_method: "Canonical structure identified"
  - normalize_metadata: "Documentation aligned"
  - verify_coherence: "Coherence restored"
  - finalize: "Ready for Conduit retry"

artifacts_produced:
  - canonical_structure_map
  - residue_disposition_ledger
  - metadata_normalization_record
  - trust_reassessment_note
  - route_recommendation

route_recommendation:
  target: "family:Conduit"
  reason: "Coherence restored - safe to synthesize"
```

### Step 7: Conduit/handoff_synthesis (Retry)

```yaml
pipeline: "Conduit/handoff_synthesis"

phases_completed:
  - scope: "Handoff for team transition"
  - sources: "Canonical sources now available"
  - structure: "Organized by canonical structure"
  - synthesize: "Handoff document created"
  - unresolveds: "Open questions documented"
  - provenance: "Full provenance recorded"
  - steps: "Next steps for new team"

artifacts_produced:
  - handoff_document.md
  - unresolveds_and_risks.yaml
  - provenance_summary.yaml
  - next_safe_steps.yaml
```

## Route History

```yaml
route_history:
  - action: "continue"
    from: null
    to: "Conduit"
    reason: "Initial request"
    
  - action: "cross_family_reroute"
    from: "Conduit"
    to: "Forensics"
    reason: "Trust collapse - documentation conflicts"
    
  - action: "cross_family_reroute"
    from: "Forensics"
    to: "Conduit"
    reason: "Coherence restored"
```

## Trust Assessment Progression

```yaml
initial_trust:
  level: "medium"  # Assumed OK before analysis
  
after_collapse:
  level: "collapsed"
  requires_defragmentation: true
  notes: "Documentation conflicts detected"
  
after_defragmentation:
  level: "high"
  coherence_restored: true
  notes: "Canonical structure established"
```

## Assertions

1. **Trust collapse handled**: System detected and responded to trust collapse
2. **Defragmentation before retry**: Coherence restored before Conduit retry
3. **Residue consulted**: Tension lens applied to interpret conflict
4. **Full provenance**: Route history captures the full journey
