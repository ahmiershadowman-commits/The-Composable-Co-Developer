# Forge — Acceptance Matrix

Exit criteria that must be satisfied before declaring a Forge pipeline complete.

## development (Frame)

| Criterion | Check | Required |
|-----------|-------|----------|
| Problem framed | `problem_frame.yaml` present with scoped description | Yes |
| Work plan produced | `work_plan.yaml` present with ordered `slices` | Yes |
| Dependencies identified | Each slice lists `dependencies` | Yes |
| Change implemented | All planned slices at `status: complete` or explicitly deferred | Yes |
| Behavior regressions checked | `regression_checks` list addressed or explicitly deferred | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: `work_plan` absent; slices not sequenced; regression checks silently skipped.

---

## coding (Shape)

| Criterion | Check | Required |
|-----------|-------|----------|
| Change scope bounded | `change_understanding.yaml` present | Yes |
| Change implemented | Code change is coherent and can be loaded/executed | Yes |
| Behavior verified | Change tested or regression risk explicitly noted | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: Change implemented without verifying no regression; scope not bounded.

---

## testing (Probe)

| Criterion | Check | Required |
|-----------|-------|----------|
| Test scope defined | Which behavior or confidence is being measured | Yes |
| Tests executed | Test results present (pass/fail/coverage) | Yes |
| Failures diagnosed | Any failing test has an identified cause | Yes |
| Confidence measured | Explicit confidence statement | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

**Failure conditions**: Tests run without diagnosing failures; confidence not stated.

---

## refactor (Temper)

| Criterion | Check | Required |
|-----------|-------|----------|
| Behavior baseline established | What must not change is stated | Yes |
| Structural change made | Refactor is complete | Yes |
| Behavior regression checked | Tests pass or regression risk documented | Yes |
| Route justified | `route_recommendation.yaml` present | Yes |

---

## Universal exit conditions (all pipelines)

1. Change is implemented and internally coherent
2. Behavior regressions checked or explicitly deferred with rationale
3. All required artifacts written to `runtime_output/Forge/<pipeline_id>/`
4. `route_recommendation.yaml` present — do not leave routing undefined
5. If trust collapses mid-build: stop, write partial artifacts, reroute to Forensics
