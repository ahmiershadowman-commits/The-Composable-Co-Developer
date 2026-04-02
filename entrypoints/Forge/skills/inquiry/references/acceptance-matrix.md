# Inquiry — Acceptance Matrix

Exit criteria that must be satisfied before declaring an Inquiry pipeline complete.

## research (Seek)

| Criterion | Check | Required |
|-----------|-------|----------|
| Question bounded | `question_frame.yaml` present with `question`, `scope`, `success_criteria` | Yes |
| Sources consulted | `source_ledger.yaml` present with sources and trust classification | Yes |
| Evidence synthesized | `synthesis_note.yaml` present | Yes |
| Gaps noted | Unresolved threads in `synthesis_note.gaps` or separate note | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: `question_frame` absent (scope undefined); sources not classified by trust; gaps silently dropped.

---

## hypothesis_generation (Venture)

| Criterion | Check | Required |
|-----------|-------|----------|
| Question framed | `question_frame.yaml` present | Yes |
| Evidence available | At least one source in `source_ledger` | Yes |
| Hypotheses generated | `hypothesis_set.yaml` with 2+ competing hypotheses | Yes |
| Hypotheses ranked | Each hypothesis has a `support_level` and `evidence` list | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: Single hypothesis (no competition); hypothesis lacking evidence support; scope not bounded.

---

## data_analysis (Read)

| Criterion | Check | Required |
|-----------|-------|----------|
| Data scoped | What data is being analyzed and why | Yes |
| Analysis performed | Statistical or structural analysis present | Yes |
| Findings stated | `analysis_report.yaml` with `findings` | Yes |
| Confidence stated | Explicit confidence or uncertainty bounds | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

*Status: experimental — not available for production use.*

---

## formalization (Bind)

| Criterion | Check | Required |
|-----------|-------|----------|
| Concepts identified | Which concepts are being formalized | Yes |
| Relations made explicit | `formal_structure.yaml` with typed relations | Yes |
| No underspecification | All symbols have definitions | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

---

## mathematics (Resolve)

| Criterion | Check | Required |
|-----------|-------|----------|
| Object language stable | Symbols are well-defined before proof begins | Yes |
| Proof/derivation complete | Each step follows from the previous | Yes |
| Counterexamples checked | If a counterexample is possible, it is surfaced | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

---

## Universal exit conditions (all pipelines)

1. Investigation scope is bounded — `question_frame` present
2. Evidence or analysis is sufficient to support all output claims
3. All required artifacts written to `runtime_output/Inquiry/<pipeline_id>/`
4. Unresolved threads explicitly noted — not silently dropped
5. If source truth becomes suspect mid-investigation: stop, reroute to Forensics
