# Inquiry Trace - Worked Example

Demonstrates Inquiry family execution with Forensics handoff.

## Scenario

Team needs to research best practices for implementing distributed caching, but first needs ground truth about current caching usage.

## Execution Flow

```
User Request → Trace → Forensics/project_mapping → Inquiry/research → Conduit/documentation
```

## Step-by-Step

### Step 1: Initial Request

```yaml
user_prompt: "Research distributed caching best practices for our API"
```

### Step 2: Trace Evaluation

```yaml
trace_decision:
  action: "cross_family_reroute"
  target: "family:Forensics"
  reason: "Need to understand current caching before research"
  intervention_band: 8
```

### Step 3: Forensics/project_mapping

```yaml
pipeline: "Forensics/project_mapping"
scope: "Map current caching usage in the codebase"

artifacts_produced:
  - inventory_ledger
  - physical_dependency_graph
  - discrepancy_ledger
  - trust_zone_map
  - route_recommendation

route_recommendation:
  target: "family:Inquiry"
  reason: "Ground truth established - ready for research"
```

### Step 4: Inquiry/research

```yaml
pipeline: "Inquiry/research"
question: "What are the best practices for distributed caching in Python APIs?"

phases:
  - frame: "Define research scope and criteria"
  - gather: "Collect sources on Redis, Memcached, etc."
  - compare: "Compare approaches"
  - synthesize: "Create recommendation"
  - gaps: "Identify open questions"
  - route: "Recommend next steps"

artifacts_produced:
  - research_findings
  - source_ledger
  - comparison_map
  - synthesis_note
  - route_recommendation
```

### Step 5: Conduit/documentation

```yaml
pipeline: "Conduit/documentation"
content: "Document caching best practices"

artifacts_produced:
  - audience_scope_note
  - documentation.md
  - route_recommendation
```

## Route History

```yaml
route_history:
  - action: "cross_family_reroute"
    from: null
    to: "Forensics"
    reason: "Need ground truth"
    
  - action: "cross_family_reroute"
    from: "Forensics"
    to: "Inquiry"
    reason: "Ready for research"
    
  - action: "cross_family_reroute"
    from: "Inquiry"
    to: "Conduit"
    reason: "Ready to document"
```

## Final Artifacts

```
runtime_output/
├── Forensics/
│   └── project_mapping/
│       ├── inventory_ledger.yaml
│       └── route_recommendation.yaml
├── Inquiry/
│   └── research/
│       ├── research_findings.yaml
│       └── source_ledger.yaml
└── Conduit/
    └── documentation/
        └── documentation.md
```

## Assertions

1. **Trace consulted first**: Trace always evaluates before any family execution
2. **Forensics before Inquiry**: Ground truth established before research
3. **Route history complete**: All transitions recorded
4. **Artifacts accumulated**: Each family produces its required artifacts
