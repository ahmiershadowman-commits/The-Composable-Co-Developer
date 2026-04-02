---
name: forge
description: >
  This skill should be used when the user asks to "build this", "implement this feature",
  "write the code for", "refactor this", "add tests", "fix this bug", "make this change",
  or any task where the primary work is shaping, modifying, or validating artifacts and
  systems. Use Forge when trustworthy state exists and the task is a concrete build or
  change operation. Also triggers on "develop", "code this up", "write tests for",
  "clean this up", "restructure without breaking behavior".
metadata:
  version: "0.2.0"
  family: Forge
---

# Forge — Build and Change Work

Forge handles all build, implementation, refactoring, and validation tasks. Only invoke Forge when the project state is trustworthy enough to act on. If trust has collapsed or the canonical structure is unclear, run Forensics first.

## When to invoke

- Bounded implementation work: writing, modifying, or extending code
- Systemic change: architectural shifts, coordinated multi-file work
- Validation: testing, failure diagnosis, confidence measurement
- Structural cleanup: refactoring without behavioral regression

Do not invoke Forge when `trust_collapse`, `docs_state_code_disagree_deeply`, or `canonical_source_unclear` are present — reroute to Forensics first.

## Pipelines

Select the smallest sufficient pipeline:

| Pipeline | Alias | Use when |
|---|---|---|
| `development` | Frame | Change scope is systemic; architecture or repo shape is in play; multiple subtasks need coordination |
| `coding` | Shape | Bounded implementation is needed; local code changes are primary |
| `testing` | Probe | Validation or failure diagnosis is primary; confidence needs explicit measurement |
| `refactor` | Temper | Structure should change without behavioral regression; local cleanup is insufficient but full development is not needed |

Default entry: `development`.

## Execution

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Forge <pipeline_id> "<problem description>"
```

Example:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" Forge coding "add rate limiting to the API client"
```

Artifacts are written to `./runtime_output/Forge/<pipeline_id>/` in your current working directory.

## After execution

Read the artifacts from `./runtime_output/Forge/<pipeline_id>/` and use them to guide the implementation. Key artifacts:

- `problem_frame` / `change_understanding` — scoped statement of what is being built
- `work_plan` / `change_plan` — ordered implementation steps
- `route_recommendation` — next step if follow-on work is needed

## If execution fails

Execute the Forge methodology directly:

1. **Frame the problem**: State exactly what is being changed and why
2. **Analyze dependencies**: Identify what the change touches and what it must not break
3. **Plan slices**: Break work into independently implementable units
4. **Implement**: Make the change using available tools (Read, Edit, Write, Bash)
5. **Validate**: Confirm the change works and hasn't regressed anything
6. **Route**: State what should happen next (test, review, deploy, or further development)

Produce the same named artifacts as structured notes.

## Exit conditions

Do not declare Forge work complete until:

1. The change is implemented and coherent
2. Behavior regressions are checked (or explicitly deferred)
3. Artifacts are written to `runtime_output/`
4. Route recommendation is surfaced if follow-on work is needed

## Pipeline feedback loops

- `development` → `coding` when implementation scope localizes
- `coding` → `testing` when behavior has changed or confidence requires validation
- `testing` → `development` when structural failure is detected
- Any Forge pipeline → Forensics when trust collapses mid-build

## References

- `references/artifacts.md` — Full artifact contracts for all Forge pipelines
- `references/acceptance-matrix.md` — Exit criteria per pipeline

## Anti-patterns

Do not continue Forge when truth has collapsed mid-build — stop and reroute to Forensics. Do not use `development` for single-file local changes (use `coding`). Do not use `refactor` when behavior change is intended.
