# /conduit

**Documentation, writing, and synthesis.**

Use this command for creating documentation, scholarly writing, professional content, and synthesizing handoff materials.

## Usage

```
/conduit [pipeline] [content or topic]
```

## Pipelines

| Pipeline | When to use |
|----------|-------------|
| `documentation` | Create or update technical documentation |
| `scholarly_writing` | Academic papers and technical articles |
| `professional_writing` | Business and professional content |
| `handoff_synthesis` | Create handoff materials for team transitions |

## Examples

```
/conduit documentation Write API documentation for the new endpoints
/conduit scholarly_writing Draft a paper on the optimization technique
/conduit professional_writing Create a project status report
/conduit handoff_synthesis Synthesize all work done for the handoff document
```

## Output

Artifacts are written to `runtime_output/` and include:
- `documentation.md` - Generated documentation
- `synthesis_report.yaml` - Synthesized findings
- `handoff_document.md` - Complete handoff materials
- `unresolveds_ledger.yaml` - Open questions and risks

## Related Commands

- `/forensics` - For understanding project state before documenting
- `/forge` - For building what you're documenting
- `/inquiry` - For research that feeds into writing
