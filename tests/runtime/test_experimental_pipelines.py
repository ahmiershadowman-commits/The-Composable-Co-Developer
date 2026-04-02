from pathlib import Path

import pytest

from runtime.execution.dispatcher import ExperimentalPipelineError, RuntimeDispatcher
from runtime.state.models import ExecutionState, FamilyType


@pytest.mark.parametrize(
    "pipeline_id",
    [
        "label_shift_correction",
        "introspection_audit",
    ],
)
def test_forensics_experimental_pipelines_blocked(pipeline_id: str):
    dispatcher = RuntimeDispatcher(Path("runtime_output"))
    state = ExecutionState(current_family=FamilyType.FORENSICS)
    with pytest.raises(ExperimentalPipelineError):
        dispatcher.execute_pipeline(FamilyType.FORENSICS, pipeline_id, state, {})


def test_forensics_experimental_pipeline_executes_with_approval():
    dispatcher = RuntimeDispatcher(Path("runtime_output"))
    state = ExecutionState(current_family=FamilyType.FORENSICS)

    result = dispatcher.execute_pipeline(
        FamilyType.FORENSICS,
        "label_shift_correction",
        state,
        {
            "experimental_approval": {
                "ticket": "EXP-001",
                "rationale": "Validate label calibration against a controlled sample.",
                "rollback_plan": "Disable calibration and restore baseline outputs.",
                "empirical_evidence": ["Offline eval on last 100 samples"],
            },
            "baseline_label_counts": {"yes": 70, "no": 30},
            "reference_label_counts": {"yes": 55, "no": 45},
            "predictions": [{"label": "yes", "score": 0.8}],
            "baseline_metric": 0.61,
            "calibrated_metric": 0.68,
        },
    )

    assert "calibration_mapping" in result.artifacts
    assert "experimental_approval" in result.metadata


def test_inquiry_experimental_pipeline_executes_with_approval():
    dispatcher = RuntimeDispatcher(Path("runtime_output"))
    state = ExecutionState(current_family=FamilyType.INQUIRY)

    result = dispatcher.execute_pipeline(
        FamilyType.INQUIRY,
        "human_hint_integration",
        state,
        {
            "experimental_approval": {
                "ticket": "EXP-002",
                "rationale": "Measure whether hints improve explanation quality.",
                "rollback_plan": "Return to model-only reasoning path.",
                "empirical_evidence": ["Blind review from pilot batch"],
            },
            "human_hints": ["Preserve the invariant around plugin-first packaging."],
            "combined_explanations": ["Integrated answer"],
            "baseline_metric": 0.44,
            "hybrid_metric": 0.57,
        },
    )

    assert "performance_comparison_report" in result.artifacts
    assert result.artifacts["adoption_decision"]["adopt"] is True
