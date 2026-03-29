#!/usr/bin/env python3
"""
Forge Family Runner - Execute Forge pipelines.

Usage:
    python entrypoints/Forge/run.py --pipeline development [--problem "description"]
"""

import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.state.models import ExecutionState, FamilyType
from runtime.artifacts.writer import ArtifactWriter
from entrypoints.Forge.executors import ForgeExecutor


def run_pipeline(pipeline_id: str, problem: str, output_dir: Path, project_root: Path = None):
    """Run a Forge pipeline."""
    project_root = project_root or Path.cwd()
    print(f"Running Forge/{pipeline_id}")
    print(f"Problem: {problem}")
    print(f"Project: {project_root}")
    print(f"Output: {output_dir}")
    print()

    state = ExecutionState(current_family=FamilyType.FORGE)
    executor = ForgeExecutor(output_dir, project_root=project_root)
    writer = ArtifactWriter(output_dir)
    
    context = {
        "problem": problem or f"Build work via {pipeline_id}",
        "constraints": [],
        "success_criteria": [],
    }
    
    try:
        if pipeline_id == "development":
            state = executor.execute_development(state, context)
        elif pipeline_id == "coding":
            state = executor.execute_coding(state, context)
        elif pipeline_id == "testing":
            state = executor.execute_testing(state, context)
        elif pipeline_id == "refactor":
            state = executor.execute_refactor(state, context)
        else:
            print(f"ERROR: Unknown pipeline: {pipeline_id}")
            return False
        
        for name, data in state.artifacts.items():
            writer.write_artifact(name, data, pipeline_id, FamilyType.FORGE)
        
        print(f"\nPipeline completed successfully")
        print(f"Artifacts produced: {list(state.artifacts.keys())}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Forge family pipelines")
    parser.add_argument("--pipeline", required=True,
                       choices=["development", "coding", "testing", "refactor"],
                       help="Pipeline to execute")
    parser.add_argument("--problem", default="", help="Problem description")
    parser.add_argument("--output", default=str(REPO_ROOT / "runtime_output"), help="Output directory")
    parser.add_argument("--project", default=str(Path.cwd()),
                        help="Project root directory (defaults to current working directory)")

    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    project_root = Path(args.project).resolve()

    success = run_pipeline(args.pipeline, args.problem, output_dir, project_root=project_root)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
