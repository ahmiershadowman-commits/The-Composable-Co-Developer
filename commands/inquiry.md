# /inquiry

**Investigation, research, and explanation.**

Use this command for deep investigation, hypothesis generation, data analysis, formal reasoning, and mathematical work.

## Usage

```
/inquiry [pipeline] [research question]
```

## Pipelines

| Pipeline | When to use |
|----------|-------------|
| `research` | Gather information and investigate a topic |
| `hypothesis_generation` | Generate testable hypotheses for a problem |
| `data_analysis` | Analyze data and extract insights |
| `formalization` | Create formal specifications or proofs |
| `mathematics` | Mathematical reasoning and calculations |

## Examples

```
/inquiry research What are the best practices for distributed caching?
/inquiry hypothesis_generation Why is the API response time degrading?
/inquiry data_analysis Analyze the error logs from last week
/inquiry formalization Specify the type system for the new DSL
/inquiry mathematics Calculate the time complexity of the algorithm
```

## Output

Artifacts are written to `runtime_output/` and include:
- `research_findings.yaml` - Gathered information and sources
- `hypothesis_ledger.yaml` - Generated hypotheses with evidence
- `analysis_report.yaml` - Data analysis results
- `formal_spec.yaml` - Formal specifications

## Related Commands

- `/forensics` - For ground-truth when state is uncertain
- `/forge` - For building after inquiry identifies the solution
- `/conduit` - For documenting research findings
