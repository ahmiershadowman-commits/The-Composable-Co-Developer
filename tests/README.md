# Tests

This bundle currently includes structural validation tests, not runtime execution tests.

## Coverage
- pipeline schema conformance
- canonical target grammar and target resolution
- family route map inventory consistency
- selector scope consistency
- worked trace presence and basic assertion checks

## Run
Use the built-in unittest runner through the helper script:

```bash
python tools/validate_bundle.py
```
