# Unresolveds Ledger

## Purpose

The unresolveds ledger tracks open questions, risks, and incomplete work that persists across pipeline executions. It ensures that uncertainty is explicitly tracked rather than lost during transitions.

## What Gets Recorded

### Unresolved Questions

Questions that remain unanswered:

```yaml
- id: UQ-001
  type: question
  description: "What is the canonical source for API documentation?"
  raised_in: "Forensics/project_mapping"
  priority: high
  blocks: ["Forge/coding", "Conduit/documentation"]
```

### Identified Risks

Potential problems that may materialize:

```yaml
- id: RISK-001
  type: risk
  description: "Test coverage below 50% for critical modules"
  raised_in: "Forge/testing"
  probability: medium
  impact: high
  mitigation: "Schedule dedicated testing sprint"
```

### Incomplete Work

Work that was started but not finished:

```yaml
- id: IW-001
  type: incomplete_work
  description: "Database migration script partially written"
  raised_in: "Forge/coding"
  completion_percentage: 60
  next_step: "Complete error handling section"
```

### Open Decisions

Decisions that were deferred:

```yaml
- id: DEC-001
  type: decision
  description: "Choose between PostgreSQL and MySQL"
  raised_in: "Forge/development"
  deadline: "2026-04-01"
  stakeholders: ["backend_team", "devops"]
  options:
    - "PostgreSQL for JSON support"
    - "MySQL for team familiarity"
```

## Ledger Structure

```yaml
unresolveds_ledger:
  questions:
    - {...}
  risks:
    - {...}
  incomplete_work:
    - {...}
  decisions:
    - {...}
  last_updated: "2026-03-25T10:30:00Z"
  total_count: 4
```

## Lifecycle

### Creation

Unresolveds are created when:

1. A pipeline identifies an open question
2. A risk is recognized but not mitigated
3. Work cannot be completed in current pipeline
4. A decision requires more information

### Tracking

Unresolveds persist in state across pipelines:

```
Pipeline 1 → Creates unresolved → State → Pipeline 2 → References unresolved
```

### Resolution

Unresolveds are resolved when:

1. Question is answered → Move to resolved ledger
2. Risk is mitigated → Update status
3. Work is completed → Remove from ledger
4. Decision is made → Record decision

## Usage in Pipelines

### Forensics

Records unresolveds about:
- Canonical source uncertainty
- Trust ambiguities
- Discrepancy explanations needed

### Forge

Records unresolveds about:
- Technical debt
- Incomplete implementations
- Testing gaps

### Inquiry

Records unresolveds about:
- Open research questions
- Evidence gaps
- Hypothesis discriminators needed

### Conduit

Records unresolveds about:
- Documentation gaps
- Handoff risks
- Stakeholder questions

## Integration with Handoff

The unresolveds ledger is a key part of handoff_synthesis:

```yaml
handoff_document:
  ...
  unresolveds_and_risks:
    high_priority:
      - "UQ-001: Canonical API docs source"
      - "RISK-001: Low test coverage"
    medium_priority:
      - "DEC-001: Database choice"
```

## Best Practices

### For Executors

1. **Record early**: Add unresolveds as soon as identified
2. **Be specific**: Clear descriptions aid resolution
3. **Track dependencies**: Note what work is blocked
4. **Update status**: Mark resolved when complete

### For Pipeline Designers

1. **Check for unresolveds**: Review at pipeline start
2. **Address high priority**: Tackle critical unresolveds first
3. **Don't create unnecessary ones**: Resolve what you can
4. **Document resolution**: Record how unresolveds were addressed

## Relationship to Other Artifacts

| Artifact | Relationship |
|----------|-------------|
| route_recommendation | Unresolveds may influence route |
| trust_assessment | Many unresolveds → lower trust |
| handoff_document | Unresolveds are included in handoff |
| provenance_summary | Tracks where unresolveds originated |
