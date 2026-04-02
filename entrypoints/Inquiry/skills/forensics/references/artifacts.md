# Forensics Artifact Contracts

After running any Forensics pipeline, read artifacts from `runtime_output/Forensics/<pipeline_id>/`.

All artifacts are YAML with a `content` field and `_provenance` (pipeline, phase, timestamp, family).

## project_mapping

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `inventory_ledger` | Complete listing of what actually exists — files, dirs, configs, runtime components |
| `physical_dependency_graph` | Actual dependency structure as observed, not as documented |
| `discrepancy_ledger` | Conflicts between sources — docs vs. code, stated vs. observed |
| `trust_zone_map` | Which areas can be trusted and which cannot, with classification rationale |
| `canonical_source_note` | What the canonical source of truth is for each contested area |
| `route_recommendation` | Recommended next family/pipeline with conditions |

**Exit check**: All 6 must be present. If `trust_zone_map` shows low trust, do not route to Forge.

## defragmentation

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `fragmentation_snapshot` | Current state of fragmentation/drift |
| `entropy_classification` | Classification: tidy / consolidate / repair / anchor |
| `chosen_method` | Which defragmentation method was selected and why |
| `residue_disposition_ledger` | What residue was preserved, cleaned, or indexed |
| `changed_structure_map` | What was actually changed and what the new structure is |
| `metadata_normalization_record` | Alignment record for metadata and provenance |
| `trust_reassessment_note` | Trust re-evaluation after defragmentation |
| `route_recommendation` | Next step now that coherence is restored |

## documentation_audit

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `documentation_inventory` | All documentation found with source and claimed scope |
| `code_state_inventory` | Actual code state as observed |
| `drift_ledger` | Where documentation has drifted from code |
| `gap_analysis` | What is in code but undocumented; what is documented but absent from code |
| `misleading_claims_ledger` | Documentation claims that are technically present but misleading |
| `audit_report` | Summary findings |
| `route_recommendation` | Next step (often Forge/Conduit to repair docs, or Inquiry to investigate gaps) |

## anomaly_disambiguation

Primary artifacts produced:

| Artifact | What it contains |
|---|---|
| `anomaly_catalog` | All anomaly signals collected |
| `anomaly_classification` | Source classification for each: data artifact, process issue, or true misfit |
| `disambiguation_options` | Candidate explanations ranked by evidence |
| `recommended_path` | Which option to pursue and why |
| `route_recommendation` | Next family (Inquiry if explanation needed; Forge if fix is clear) |

## Routing guide

After reading `route_recommendation`, route to:
- `family:Forensics/defragmentation` — entropy is primary
- `family:Forge` — state is grounded, build work can proceed
- `family:Inquiry` — state is grounded but explanation is missing
- `family:Conduit` — communication or handoff is now primary
