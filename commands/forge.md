# /forge

**Build and change work with structured methodology.**

Use this command for implementation tasks: developing new features, writing code, creating tests, or refactoring existing code.

## Usage

```
/forge [pipeline] [problem description]
```

## Pipelines

| Pipeline | When to use |
|----------|-------------|
| `development` | Plan and architect build work before coding |
| `coding` | Implement code changes and new features |
| `testing` | Create tests and validate implementations |
| `refactor` | Restructure existing code without changing behavior |

## Examples

```
/forge development Build a user authentication system with JWT tokens
/forge coding Add rate limiting to the API endpoints
/forge testing Create integration tests for the payment flow
/forge refactor Extract the validation logic into a separate module
```

## Output

Artifacts are written to `runtime_output/` and include:
- `work_plan.yaml` - Structured development plan
- `architecture_note.yaml` - Architecture decisions
- `change_plan.yaml` - Detailed change specification
- `validation_note.yaml` - Validation results

## Related Commands

- `/forensics` - Use before Forge when project state is unclear
- `/inquiry` - For research and analysis before building
- `/conduit` - For documentation after build work is complete
