# Forge Artifact Contracts

After running any Forge pipeline, read artifacts from `runtime_output/Forge/<pipeline_id>/`.

## development

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `problem_frame` | Scoped statement of what is being built and why |
| `architecture_note` | Architectural decisions made and rationale |
| `work_plan` | Ordered task breakdown with dependencies |
| `slice_map` | How the work divides into implementable slices |
| `verification_summary` | How correctness will be confirmed |
| `route_recommendation` | Next step (usually pipeline:Forge/coding) |

**Use when**: Change scope is systemic, architecture is in play, or multiple subtasks need coordination.

## coding

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `change_understanding` | What the change actually requires |
| `change_plan` | How the change will be implemented |
| `changed_artifact` | The actual code or artifact produced |
| `validation_note` | Evidence that the change works as intended |
| `route_recommendation` | Next step (often pipeline:Forge/testing) |

**Use when**: Bounded implementation work; local code changes are primary.

## testing

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `test_scope` | What is being tested and why |
| `test_strategy` | How tests are structured and what they cover |
| `test_results` | Pass/fail outcomes with diagnostic detail |
| `test_report` | Summary findings and confidence assessment |
| `route_recommendation` | Next step (Forge/development if structural failure; done if passing) |

**Use when**: Validation or failure diagnosis is primary; confidence needs explicit measurement.

## refactor

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `current_shape_map` | Current structure as it exists |
| `invariants_ledger` | What behaviors must not change |
| `refactor_plan` | How structure will change while preserving invariants |
| `refactored_artifact` | The refactored code or structure |
| `behavior_validation` | Evidence that invariants were preserved |
| `route_recommendation` | Next step |

**Use when**: Structure should change without behavioral regression; local cleanup is insufficient but full development is not needed.

## Forge→Forensics trigger

If any of the following appear mid-pipeline, stop and reroute to Forensics:
- `trust_collapse` — the ground truth can no longer be assumed
- `docs_state_code_disagree_deeply` — canonical source is unclear
- `canonical_source_unclear` — what to build from is ambiguous
