# Validation Report

## Summary

- pipeline files checked: 21
- selector files checked: 4
- family route maps checked: 4
- primitives resolved: 12
- operators resolved: 4
- evaluators resolved: 6

## Results

### Pipeline schema failures
[]

### Route map failures
[]

### Selector scope failures
[]

### Target grammar / resolution failures
[]

## Verdict

This bundle now passes the normalization checks implemented in this pass:

- canonical pipeline grammar present
- route maps synchronized with live inventory
- selector scopes synchronized with core route maps
- target strings normalized to canonical grammar
- target references resolve against current primitives, operators, evaluators, families, and pipelines

This validation is still structural, not semantic execution.
The next layer would be:
- schema tests
- route simulation tests
- worked example assertion tests
