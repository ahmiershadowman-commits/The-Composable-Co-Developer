#!/usr/bin/env python3
"""
Inquiry Family Runner - Execute Inquiry pipelines.

Usage:
    python entrypoints/Inquiry/run.py --pipeline research [--question "question"]
"""

import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.state.models import ExecutionState, FamilyType
from runtime.artifacts.writer import ArtifactWriter
from entrypoints.Inquiry.executors import InquiryExecutor


def run_pipeline(pipeline_id: str, question: str, output_dir: Path, project_root: Path = None):
    """Run an Inquiry pipeline."""
    project_root = project_root or Path.cwd()
    print(f"Running Inquiry/{pipeline_id}")
    print(f"Question: {question}")
    print(f"Project: {project_root}")
    print(f"Output: {output_dir}")
    print()

    state = ExecutionState(current_family=FamilyType.INQUIRY)
    executor = InquiryExecutor(output_dir)
    writer = ArtifactWriter(output_dir)

    context = {
        "question": question or f"Investigation via {pipeline_id}",
        "project_root": str(project_root),
        "hypotheses": [],
        "evidence_sources": [],
    }
    
    try:
        if pipeline_id == "research":
            state = executor.execute_research(state, context)
        elif pipeline_id == "hypothesis_generation":
            state = executor.execute_hypothesis_generation(state, context)
        elif pipeline_id == "data_analysis":
            state = executor.execute_data_analysis(state, context)
        elif pipeline_id == "formalization":
            state = executor.execute_formalization(state, context)
        elif pipeline_id == "mathematics":
            state = executor.execute_mathematics(state, context)
        else:
            print(f"ERROR: Unknown pipeline: {pipeline_id}")
            return False
        
        for name, data in state.artifacts.items():
            writer.write_artifact(name, data, pipeline_id, FamilyType.INQUIRY)
        
        print(f"\nPipeline completed successfully")
        print(f"Artifacts produced: {list(state.artifacts.keys())}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Inquiry family pipelines")
    parser.add_argument("--pipeline", required=True,
                       choices=["research", "hypothesis_generation", "data_analysis", "formalization", "mathematics"],
                       help="Pipeline to execute")
    parser.add_argument("--question", default="", help="Research question")
    parser.add_argument("--output", default=str(REPO_ROOT / "runtime_output"), help="Output directory")
    parser.add_argument("--project", default=str(Path.cwd()),
                        help="Project root directory (defaults to current working directory)")

    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    project_root = Path(args.project).resolve()

    success = run_pipeline(args.pipeline, args.question, output_dir, project_root=project_root)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
