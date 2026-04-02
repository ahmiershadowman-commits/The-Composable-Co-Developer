"""Render an HTML execution report from a lightweight runtime state payload."""

import argparse
import json
from pathlib import Path

import yaml

from runtime.state.models import ExecutionState, FamilyType
from runtime.visualization.report import RuntimeReportRenderer


def _load_payload(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a runtime HTML report.")
    parser.add_argument("--input", required=True, help="Path to YAML/JSON payload")
    parser.add_argument("--family", required=True, choices=[item.value for item in FamilyType])
    parser.add_argument("--pipeline", required=True, help="Pipeline identifier")
    parser.add_argument(
        "--output-dir",
        default="runtime_output",
        help="Directory where the HTML report should be written",
    )
    args = parser.parse_args()

    payload = _load_payload(Path(args.input)) or {}
    state = ExecutionState(
        current_family=FamilyType(args.family),
        current_pipeline=args.pipeline,
    )
    for key, value in payload.get("artifacts", {}).items():
        state.add_artifact(key, value)
    for key, value in payload.get("metadata", {}).items():
        state.add_metadata(key, value)
    for error in payload.get("errors", []):
        state.add_error(str(error))

    renderer = RuntimeReportRenderer(Path(args.output_dir))
    report_path = renderer.render(args.family, args.pipeline, state)
    print(f"Wrote runtime report to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
