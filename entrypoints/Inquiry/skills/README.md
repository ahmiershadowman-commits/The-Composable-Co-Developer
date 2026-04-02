# Skills Package

Executable skills for The Composable Co-Developer marketplace.

## Available Skills

| Skill | Purpose |
|-------|---------|
| `forensics` | Ground-truth establishment |
| `forge` | Build and change work |
| `inquiry` | Investigation and research |
| `conduit` | Documentation and synthesis |

## Usage

Import skills in your code:

```python
from skills.forensics import run_forensics
from skills.forge import run_forge
from skills.inquiry import run_inquiry
from skills.conduit import run_conduit
```

## Example

```python
# Run forensics to map project state
result = run_forensics(
    pipeline="project_mapping",
    scope="Map the authentication module"
)

if result["success"]:
    print(f"Artifacts written to: {result['output_dir']}")
else:
    print(f"Error: {result.get('error', result.get('stderr'))}")
```

## Output

All skills write artifacts to `runtime_output/` directory by default.
