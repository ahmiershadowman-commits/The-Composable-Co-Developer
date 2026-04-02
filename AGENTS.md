# AGENTS.md — Agent Coding Guidelines

This file provides coding guidelines and commands for agents working in this repository.

## Build, Test, and Validation Commands

### Running Tests

```bash
# All tests
python -m pytest tests -v --tb=short

# Single test file
python -m pytest tests/runtime/test_registry_load.py -v

# Single test method
python -m pytest tests/runtime/test_registry_load.py::TestRegistryLoad::test_registry_loads -v

# Tests with coverage
python -m pytest tests --cov=. --cov-report=html

# Specific test category
python -m pytest tests/runtime/ -v      # Runtime tests
python -m pytest tests/routing/ -v      # Routing tests
python -m pytest tests/schemas/ -v      # Schema tests
python -m pytest tests/worked_examples/ -v  # Worked examples
```

### Validation Tools

```bash
# End-to-end vertical slice (Forensics → Forge)
python tools/run_vertical_slice.py

# Bundle validation (runs pytest)
python tools/validate_bundle.py
```

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate
```

## Code Style Guidelines

### General Conventions

- Follow **PEP 8** style guidelines
- Use **type hints** for all function signatures
- Write **docstrings** for public methods (Google-style)
- Keep functions focused and small (< 50 lines preferred)
- Use **unittest.TestCase** for tests

### Imports

```python
# Standard library first, then third-party, then local
import ast
import re
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from runtime.state.models import ExecutionState, TrustAssessment, FamilyType
from runtime.artifacts.writer import ArtifactWriter
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `ExecutionState`, `SpecRegistry`)
- **Functions/methods**: `snake_case` (e.g., `execute_project_mapping`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `_CODE_EXTS`)
- **Private functions**: prefix with `_` (e.g., `_classify_file`)
- **Enums**: suffix with `Type` or use descriptive names (e.g., `FamilyType`, `RouteAction`)

### Type Hints

Use explicit type hints:
```python
def execute_project_mapping(
    state: ExecutionState,
    context: Dict[str, Any],
    output_path: Path,
    project_root: Optional[Path] = None,
) -> ExecutionState:
```

### Dataclasses

Use `@dataclass` for data containers:
```python
@dataclass
class RuntimeContext:
    repo_root: Path
    bundle_path: Path
    output_path: Path
    family: FamilyType
    pipeline_id: Optional[str] = None
    phase_id: Optional[str] = None
```

### Error Handling

- Use custom exceptions from `runtime/errors/errors.py`
- Raise specific exception types with clear messages
- Log errors in state via `state.add_error()`

### YAML Specifications

- All pipeline specs must conform to `runtime/schemas/pipeline.yaml`
- Use canonical target grammar: `primitive:`, `operator:`, `pipeline:Family/id`, `family:`, `authority:`
- Frame aliases are frontmatter only — never use as runtime identifiers

### Test Structure

```python
import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.registry.loader import SpecRegistry


class TestRegistryLoad(unittest.TestCase):
    """Test registry loading."""
    
    def setUp(self):
        self.registry = SpecRegistry(REPO_ROOT)
    
    def test_registry_loads(self):
        """Test that registry loads without errors."""
        index = self.registry.load_all()
        self.assertIsInstance(index, SpecIndex)


if __name__ == "__main__":
    unittest.main()
```

### File Organization

- **Runtime**: `runtime/` — core execution spine
- **Entrypoints**: `entrypoints/<Family>/executors.py` — family pipeline executors
- **Shared**: `shared/` — primitives, operators, authorities (Trace, Lever, Residue)
- **Tests**: `tests/` — organized by category (runtime, routing, schemas, worked_examples)

### Key Project Principles

1. **Dependency Law**: Forge/Inquiry/Conduit cannot proceed without Forensics establishing ground truth first
2. **Smallest-Sufficient Intervention**: Use minimal intervention (motif → primitive → evaluator → reroute → forensics_reset)
3. **Artifact Immutability**: Artifacts are added, not modified; always include provenance
4. **Residue Preservation**: Preserve oddities when rerouting between families

### Commit Convention

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Build/config changes

### Running CI Locally

```bash
# Full CI simulation (runs on windows-latest with Python 3.10-3.12)
python -m pytest tests -v --tb=short
python tools/run_vertical_slice.py
python tools/validate_bundle.py
```
