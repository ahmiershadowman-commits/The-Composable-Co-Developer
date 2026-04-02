#!/usr/bin/env python3
"""Forge family runner."""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.artifacts.writer import ArtifactWriter
from runtime.execution.dispatcher import RuntimeDispatcher
from runtime.state.models import ExecutionState, FamilyType


PRIMARY_CONTEXT_KEY = "problem"
FAMILY = FamilyType.FORGE
PIPELINE_CHOICES = ['development', 'coding', 'testing', 'refactor']


def _load_json_payload(raw_value: str):
    """Load JSON from an inline string or a file path."""
    if not raw_value:
        return None
    candidate = Path(raw_value)
    if candidate.exists():
        return json.loads(candidate.read_text(encoding="utf-8"))
    return json.loads(raw_value)


def run_pipeline(
    pipeline_id: str,
    primary_value: str,
    output_dir: Path,
    project_root: Path,
    approval_json: str = "",
    render_report: bool = False,
    required_mcp=None,
    connect_all_mcp: bool = False,
):
    """Run one family pipeline through the shared runtime dispatcher."""
    print(f"Running Forge/{pipeline_id}")
    print(f"Problem: {primary_value}")
    print(f"Project: {project_root}")
    print(f"Output: {output_dir}")
    print()

    state = ExecutionState(current_family=FAMILY)
    writer = ArtifactWriter(output_dir)
    dispatcher = RuntimeDispatcher(output_dir)

    context = {
        PRIMARY_CONTEXT_KEY: primary_value or f"Forge execution via {pipeline_id}",
        "project_root": str(project_root),
        "render_report": render_report,
        "required_mcp": required_mcp or [],
        "connect_all_mcp": connect_all_mcp,
    }

    if FAMILY == FamilyType.FORENSICS:
        context["scope"] = {
            "description": primary_value or f"Forge execution via {pipeline_id}",
            "boundaries": [],
        }
    if approval_json:
        context["experimental_approval"] = _load_json_payload(approval_json)

    try:
        state = dispatcher.execute_pipeline(FAMILY, pipeline_id, state, context)
        for name, data in state.artifacts.items():
            writer.write_artifact(name, data, pipeline_id, FAMILY)

        print("\nPipeline completed")
        print(f"Artifacts produced: {list(state.artifacts.keys())}")
        if state.metadata:
            print(f"Metadata: {list(state.metadata.keys())}")
        if state.errors:
            print(f"Errors: {state.errors}")
            return False
        return True
    except Exception as exc:
        print(f"ERROR: {exc}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Forge family pipelines")
    parser.add_argument("--pipeline", required=True, choices=PIPELINE_CHOICES, help="Pipeline to execute")
    parser.add_argument("--problem", default="", help="Primary pipeline input")
    parser.add_argument("--output", default=str(REPO_ROOT / "runtime_output"), help="Output directory")
    parser.add_argument("--project", default=str(Path.cwd()), help="Project root to analyze")
    parser.add_argument("--approval-json", default="", help="Inline JSON or path to a JSON file for experimental approval")
    parser.add_argument("--render-report", action="store_true", help="Render an HTML runtime report")
    parser.add_argument("--require-mcp", action="append", dest="required_mcp", help="Managed MCP name to probe before execution")
    parser.add_argument("--connect-all-mcp", action="store_true", help="Probe all managed MCP definitions before execution")

    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    project_root = Path(args.project).resolve()

    success = run_pipeline(
        args.pipeline,
        getattr(args, PRIMARY_CONTEXT_KEY),
        output_dir,
        project_root,
        approval_json=args.approval_json,
        render_report=args.render_report,
        required_mcp=args.required_mcp,
        connect_all_mcp=args.connect_all_mcp,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
