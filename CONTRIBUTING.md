# Contributing to The Composable Co-Developer

Thank you for considering contributing to the Composable Co-Developer marketplace!

## Development Setup

1. **Fork and clone**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/the-composable-co-developer.git
   cd the-composable-co-developer
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov  # For testing
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write docstrings for public methods
- Keep functions focused and small

## Testing

### Running Tests

```bash
# All tests
python -m pytest tests -v

# With coverage
python -m pytest tests --cov=. --cov-report=html

# Specific test file
python -m pytest tests/runtime/test_registry_load.py -v
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test method names
- Test both success and failure cases

## Adding New Components

### New Pipeline

1. Create directory: `entrypoints/<Family>/pipelines/<pipeline_name>/`
2. Add `pipeline.yaml` spec following the schema
3. Implement executor method in `entrypoints/<Family>/executors.py`
4. Update dispatcher in `runtime/execution/dispatcher.py`
5. Add tests

### New Operator

1. Create `shared/operators/<operator_name>.yaml`
2. Add to `shared/operators/registry.yaml`
3. Document in `shared/operators/README.md`
4. Add tests for operator loading

### New Motif

1. Create `shared/motifs/<motif_name>.yaml`
2. Add to `shared/motifs/registry.yaml`
3. Document usage in `docs/architecture/motif_layer_rationale.md`

### New Documentation

1. Place in appropriate `docs/` subdirectory
2. Use markdown format
3. Add to relevant index files

## Pull Request Process

1. **Create branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following existing patterns

3. **Run tests**:
   ```bash
   python -m pytest tests -v
   ```

4. **Commit** with clear messages:
   ```bash
   git commit -m "feat: add new operator for comparison"
   ```

5. **Push and open PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Build/config changes

## Architecture Guidelines

### Follow the Dependency Law

- Forensics before trust-dependent work
- Trace before escalation
- Lever after Trace
- Resolution before transitions

### Use Canonical Grammar

- `primitive:<name>`
- `operator:<name>`
- `evaluator:<name>`
- `pipeline:<Family>/<id>`
- `family:<Family>`
- `authority:<Trace|Lever|Residue>`
- `forensics_reset`

### Maintain Artifact Immutability

- Artifacts are added, not modified
- Use versioned names for iterations
- Include provenance in all artifacts

## Questions?

- Check [BUILD_CONTRACT.md](BUILD_CONTRACT.md) for architecture specs
- Review [docs/](docs/) for implementation details
- Look at existing components for patterns

## Code of Conduct

Be respectful and inclusive in all interactions.
