# Forge Build Plan

## Why Forge is next

Forge is the first build/change family and depends directly on Forensics to avoid
building on bad ground truth.

## Scope

### Core pipelines
- `development`
- `coding`
- `testing`
- `refactor`

## Build order inside Forge

### 1. Development
Implements system-level shaping, coordination, and work slicing.

Must produce:
- work plan
- architecture note
- slice map
- verification summary
- handoff or release note

### 2. Coding
Implements bounded local artifact change.

Must produce:
- change plan
- changed artifact record
- validation note
- local fit note
- route recommendation

### 3. Testing
Implements explicit validation and defect classification.

Must produce:
- target matrix
- test strategy
- test results
- defect classification
- repair or route plan
- test report

### 4. Refactor
Implements structural reshaping while preserving intended behavior.

Must produce:
- current shape map
- invariants ledger
- refactor plan
- behavior validation report
- route recommendation

## Route requirements

Forge must be able to:
- accept entry only when truth is grounded enough
- shift from development -> coding -> testing
- shift from coding -> development when scope expands
- shift from testing -> development when failure is structural
- reroute to Forensics on trust collapse
- reroute to Conduit when communication/handoff becomes primary

## Acceptance criteria

- Forge never outruns Forensics when trust is uncertain
- bounded coding stays bounded
- development coordinates multi-slice work
- testing classifies failures well enough to route correctly
- refactor remains distinct from generic implementation
