# Worked Trace: Forensics → Defragmentation → Forge

## Scenario

A repo is handed over with:
- multiple READMEs
- conflicting setup notes
- duplicate config files
- tests failing in different ways
- documentation that claims a canonical structure that no longer matches the tree

The task request is “please continue development.”

## Step 1 — Enter Forensics/project_mapping

Reason:
The request sounds like Forge work, but the state surface is not yet trustworthy.

Trace checks:
- Is current family fit safe? → no
- Is there trust collapse? → yes
- Smallest sufficient action? → family:Forensics

Artifacts produced:
- inventory_ledger
- physical_dependency_graph
- discrepancy_ledger
- trust_zone_map
- canonical_source_note

Finding:
Entropy and canonical conflict are primary.

Route:
- `pipeline:Forensics/defragmentation`

## Step 2 — Forensics/defragmentation

Method selection:
- not just tidy
- not just consolidate
- repair + anchor risk present

Chosen method:
- `method:anchor`

Reason:
There is no single currently trustworthy canonical state.

Actions:
- archive superseded docs
- identify highest-trust config lineage
- normalize metadata pointers
- produce changed structure map
- produce trust reassessment note

Artifacts produced:
- residue_disposition_ledger
- metadata_normalization_record
- trust_reassessment_note
- route_recommendation

Return:
- `pipeline:Forensics/project_mapping`

## Step 3 — Recheck in Forensics/project_mapping

Reason:
Defragmentation restored coherence, but truth must be re-established before build work.

Outcome:
- canonical source is now bounded
- discrepancy surface is reduced
- route recommendation now points to Forge

Route:
- `family:Forge`

## Step 4 — Enter Forge/development

Reason:
The issue is no longer purely local code editing.
There are multiple work slices:
- config repair
- dependency cleanup
- doc alignment
- local code changes

Trace micro-checks:
- implementation localized yet? → partially
- docs mismatch still blocking? → low enough to proceed
- need sibling pipeline? → yes

Route inside family:
- `pipeline:Forge/coding` for bounded implementation
- later `pipeline:Forge/testing`

## Step 5 — Forge/coding

Work:
- perform local code changes against the newly grounded structure
- preserve metadata update record
- produce validation note

Finding:
Bounded change completed; behavior changed.

Sibling shift:
- `pipeline:Forge/testing`

## Step 6 — Forge/testing

Work:
- run validation against the now-grounded artifact
- classify failures

If failures are local:
- return to `pipeline:Forge/coding`

If failures are structural:
- return to `pipeline:Forge/development`

If truth collapses again:
- route to `family:Forensics`

## Why this worked

- The system did not trust documentation at face value.
- It did not jump straight into coding.
- It used the smallest sufficient escalation:
  - trust collapse → Forensics
  - entropy primary → Defragmentation
  - coherence restored → Forensics recheck
  - safe build state → Forge
  - bounded local change → Coding
  - explicit validation → Testing

## Load-bearing distinction preserved

- **Forensics** established truth.
- **Defragmentation** restored coherence.
- **Trace** supervised interventions and prevented premature build work.
- **Forge** resumed only after the surface became trustworthy again.
