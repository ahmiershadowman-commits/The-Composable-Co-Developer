# Tests

This bundle includes structural validation tests and runtime execution tests.

## Coverage
- pipeline schema conformance
- canonical target grammar and target resolution
- family route map inventory consistency
- selector scope consistency
- registry loading and target resolution
- transition engine behavior
- vertical slice execution
- worked trace presence and assertions

## Run

### Full test suite (recommended)
```bash
python -m pytest tests -v
```

### Using validation script
```bash
python tools/validate_bundle.py
```

### With coverage
```bash
python -m pytest tests --cov=. --cov-report=html
```

### Specific test module
```bash
python -m pytest tests/runtime/test_registry_load.py -v
```
