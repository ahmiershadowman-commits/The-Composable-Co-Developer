from pathlib import Path

from runtime.state.models import ExecutionState, FamilyType
from runtime.visualization.report import RuntimeReportRenderer


def test_runtime_report_renderer_writes_html(tmp_path):
    state = ExecutionState(current_family=FamilyType.FORGE, current_pipeline="coding")
    state.add_artifact("work_plan", {"steps": ["change", "test"]})
    state.add_metadata("managed_mcp_sessions", {"github-managed": {"connected": True}})

    renderer = RuntimeReportRenderer(tmp_path)
    report_path = renderer.render("Forge", "coding", state)

    assert report_path.exists()
    html = report_path.read_text(encoding="utf-8")
    assert "Forge / coding" in html
    assert "work_plan" in html
