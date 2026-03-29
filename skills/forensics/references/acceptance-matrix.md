# Forensics — Acceptance Matrix

Exit criteria that must be satisfied before declaring a Forensics pipeline complete.

## project_mapping (Survey)

| Criterion | Check | Required |
|-----------|-------|----------|
| Scope is bounded | `scope_note.yaml` present with `scope` field | Yes |
| Inventory complete | `inventory_ledger.yaml` present with `artifacts` array populated | Yes |
| Provenance classified | `provenance_ledger.yaml` present | Yes |
| Dependency graph constructed | `physical_dependency_graph.yaml` present with `nodes` and `edges` | Yes |
| Discrepancies mapped | `discrepancy_ledger.yaml` present | Yes |
| Trust zones classified | `trust_zone_map.yaml` present with `overall_trust` and `zones` | Yes |
| Route justified | `route_recommendation.yaml` present with `recommended_next` | Yes |
| No silent drops | All unresolved discrepancies appear in `discrepancy_ledger` | Yes |

**Failure conditions**: Any required artifact missing; `trust_zone_map.yaml` absent (blocks Forge/Inquiry gate hook); `route_recommendation` lacking rationale.

---

## defragmentation (Gather)

| Criterion | Check | Required |
|-----------|-------|----------|
| Entropy classified | `entropy_classification.yaml` present with `severity` | Yes |
| Method chosen | `chosen_method.yaml` present with `method` and `actions` | Yes |
| Changes documented | `changed_structure_map.yaml` present | Yes |
| Residue disposed | `residue_disposition_ledger.yaml` present | Yes |
| Coherence verified | `trust_reassessment_note.yaml` present with `coherence_status` | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |
| No orphaned state | `coherence_status != "not_restored"` OR re-rerouted to defragmentation | Yes |

**Failure conditions**: `coherence_status = "not_restored"` without re-reroute; changed_structure_map absent.

---

## documentation_audit (Reconcile)

| Criterion | Check | Required |
|-----------|-------|----------|
| Doc inventory complete | `documentation_inventory.yaml` present | Yes |
| Code state inventoried | `code_state_inventory.yaml` present | Yes |
| Drift detected | `drift_ledger.yaml` present | Yes |
| Gaps identified | `gap_analysis.yaml` present | Yes |
| Misleading claims surfaced | `misleading_claims_ledger.yaml` present | Yes |
| Audit report produced | `audit_report.yaml` present | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

---

## anomaly_disambiguation (Isolate)

| Criterion | Check | Required |
|-----------|-------|----------|
| Anomalies surfaced | `anomaly_catalog.yaml` present with `anomalies` array | Yes |
| Anomalies classified | `anomaly_classification.yaml` with `primary_type` | Yes |
| Options generated | `disambiguation_options.yaml` present | Yes |
| Path recommended | `recommended_path.yaml` with `recommended_option` | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

---

## Universal exit conditions (all pipelines)

1. All required artifacts are written to `runtime_output/Forensics/<pipeline_id>/`
2. `route_recommendation.yaml` present with `recommended_next` and `rationale`
3. No unresolved threads silently dropped — surfaces in appropriate ledger
4. Trust classification is explicit (not "unknown")
