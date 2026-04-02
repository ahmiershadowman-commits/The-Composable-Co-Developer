"""HTML report rendering for runtime executions."""

from html import escape
from pathlib import Path
from typing import Any, Dict

from runtime.state.models import ExecutionState


class RuntimeReportRenderer:
    """Render a minimal HTML report for one execution state."""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)

    def render(
        self,
        family: str,
        pipeline_id: str,
        state: ExecutionState,
    ) -> Path:
        """Render one HTML report and return the file path."""
        report_dir = self.output_dir / "_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{family.lower()}_{pipeline_id}.html"

        html = self._build_html(family, pipeline_id, state)
        report_path.write_text(html, encoding="utf-8")
        return report_path

    def _build_html(
        self,
        family: str,
        pipeline_id: str,
        state: ExecutionState,
    ) -> str:
        artifacts = "\n".join(
            f"<li><strong>{escape(name)}</strong><pre>{escape(self._preview(value))}</pre></li>"
            for name, value in state.artifacts.items()
        ) or "<li>No artifacts recorded.</li>"
        errors = "\n".join(f"<li>{escape(error)}</li>" for error in state.errors) or "<li>None</li>"
        metadata = "\n".join(
            f"<li><strong>{escape(key)}:</strong> {escape(self._preview(value))}</li>"
            for key, value in state.metadata.items()
        ) or "<li>None</li>"

        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(family)} / {escape(pipeline_id)} report</title>
  <style>
    body {{ font-family: Georgia, 'Times New Roman', serif; margin: 2rem; background: #f4efe6; color: #1f1a17; }}
    main {{ max-width: 980px; margin: 0 auto; background: #fffaf2; border: 1px solid #d6c7af; padding: 2rem; }}
    h1, h2 {{ margin-bottom: 0.5rem; }}
    .meta {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
    .panel {{ background: #fff; border: 1px solid #e5d8c1; padding: 1rem; }}
    pre {{ white-space: pre-wrap; word-break: break-word; margin: 0.5rem 0 0; }}
  </style>
</head>
<body>
  <main>
    <h1>{escape(family)} / {escape(pipeline_id)}</h1>
    <p>Runtime execution report for the Claude Code plugin-first bundle.</p>
    <section class="meta">
      <div class="panel">
        <h2>State</h2>
        <ul>
          <li><strong>Current family:</strong> {escape(state.current_family.value)}</li>
          <li><strong>Current pipeline:</strong> {escape(state.current_pipeline or pipeline_id)}</li>
          <li><strong>Current phase:</strong> {escape(state.current_phase or "n/a")}</li>
          <li><strong>Route decisions:</strong> {len(state.route_history)}</li>
        </ul>
      </div>
      <div class="panel">
        <h2>Metadata</h2>
        <ul>{metadata}</ul>
      </div>
    </section>
    <section class="panel">
      <h2>Errors</h2>
      <ul>{errors}</ul>
    </section>
    <section class="panel">
      <h2>Artifacts</h2>
      <ul>{artifacts}</ul>
    </section>
  </main>
</body>
</html>
"""

    def _preview(self, value: Any) -> str:
        """Return a compact preview string."""
        text = str(value)
        return text if len(text) <= 400 else text[:397] + "..."
