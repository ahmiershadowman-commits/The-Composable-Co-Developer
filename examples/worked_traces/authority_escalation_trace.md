# Authority Escalation Trace - Worked Example

Demonstrates the full Trace → Residue → Lever escalation chain.

## Scenario

Conflicting requirements create tension that requires evaluator adjudication.

## Execution Flow

```
User Request → Trace → Residue (lens) → Lever (evaluator) → Commitment Decision
```

## Step-by-Step

### Step 1: Initial Request

```yaml
user_prompt: "Should we use PostgreSQL or MySQL for the new service?"
```

### Step 2: Trace Evaluation

```yaml
trace_decision:
  action: "continue"
  target: "family:Inquiry"
  reason: "Decision requires research"
  intervention_band: 2
  
detected_patterns:
  - motif: "watershed"  # High-stakes decision
  - motif: "tension"    # Conflicting opinions
```

### Step 3: Residue Consultation

```yaml
residue_lens: "tension"
interpretation: "Active disagreement between team members"
recommendation: "Requires explicit adjudication"

residue_output:
  tension_type: "technical_choice"
  stakeholders: ["backend_team", "devops"]
  options: ["PostgreSQL", "MySQL"]
```

### Step 4: Trace Determines Evaluator Needed

```yaml
trace_decision:
  action: "authority_call"
  target: "authority:Lever"
  reason: "Tension requires evaluator adjudication"
  intervention_band: 4
  
escalation_reason: "Discriminator required between options"
```

### Step 5: Lever Escalation

```yaml
lever_action: "escalate"
evaluator: "discriminator_evaluator"

evaluator_input:
  options:
    - name: "PostgreSQL"
      pros: ["JSON support", "Advanced features"]
      cons: ["Learning curve"]
    - name: "MySQL"
      pros: ["Team familiarity", "Simpler"]
      cons: ["Limited JSON"]

evaluator_output:
  discriminators:
    - "JSON requirement is key differentiator"
    - "Team familiarity reduces initial velocity risk"
  recommendation: "PostgreSQL if JSON needed, MySQL otherwise"
```

### Step 6: Lever Commitment Decision

```yaml
lever_decision:
  type: "commit_with_conditions"
  commitment: "PostgreSQL"
  conditions:
    - "JSON data requirements confirmed"
    - "Team training scheduled"
  
reopen_rule:
  trigger: "JSON requirements change"
  action: "Re-evaluate with new constraints"
```

### Step 7: Route to Implementation

```yaml
trace_decision:
  action: "cross_family_reroute"
  target: "family:Forge"
  reason: "Decision made - ready to implement"
  intervention_band: 8
```

## Route History

```yaml
route_history:
  - action: "continue"
    from: null
    to: "Inquiry"
    reason: "Research requested"
    
  - action: "authority_call"
    from: "Inquiry"
    to: "Lever"
    reason: "Evaluator adjudication needed"
    
  - action: "cross_family_reroute"
    from: "Lever"
    to: "Forge"
    reason: "Decision made - implement"
```

## Authority Interaction Summary

```
Trace (initial eval)
  ↓
Residue (tension lens)
  ↓
Trace (escalate to Lever)
  ↓
Lever (discriminator_evaluator)
  ↓
Lever (commitment decision)
  ↓
Trace (route to Forge)
```

## Assertions

1. **Trace first**: Trace evaluated before any authority consultation
2. **Residue for interpretation**: Residue interpreted the tension pattern
3. **Lever for adjudication**: Only Lever can make commitment decisions
4. **Correct order**: Trace → Residue → Lever → Commitment (not skipped)
