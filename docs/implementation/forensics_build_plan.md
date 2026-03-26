# Forensics Build Plan

## Why Forensics comes first among families

Forensics is the only deep truth-establishing entrypoint.
If it is not real, every other family risks operating on a false or merely assumed surface.

## Scope

### Core pipelines
- `project_mapping`
- `defragmentation`
- `documentation_audit`
- `anomaly_disambiguation`

### Experimental (parked for now)
- `label_shift_correction`
- `introspection_audit`

## Build order inside Forensics

### 1. Project mapping
Implement first.

Must produce:
- inventory ledger
- physical dependency graph
- discrepancy ledger
- trust zone map
- canonical source note
- route recommendation

### 2. Defragmentation
Implement second.

Must support methods:
- tidy
- consolidate
- repair
- anchor

Must produce:
- entropy classification
- residue disposition ledger
- metadata normalization record
- trust reassessment note
- route recommendation

### 3. Documentation audit
Implement third.

Must compare:
- doc claims
- observed state

Must produce:
- claim ledger
- docs trust assessment
- reconciliation map
- route recommendation

### 4. Anomaly disambiguation
Implement fourth.

Must classify whether anomaly is:
- real signal
- artifact
- frame mismatch
- trust problem
- distribution problem

Must produce:
- anomaly classification
- trust/distribution assessment
- route recommendation

## Route requirements

Forensics must be able to:
- enter from any family on trust collapse
- route to Defragmentation when entropy is primary
- return to project mapping after Defragmentation recheck
- hand off to Forge / Inquiry / Conduit with grounded route recommendation

## Acceptance criteria

- Forensics can establish truth before other families act
- Defragmentation changes are followed by recheck
- Documentation audit can prevent false doc trust
- Anomaly disambiguation can sort signal from noise before explanation
