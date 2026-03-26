#!/usr/bin/env python3
"""
Conduit Family Runner - Execute Conduit pipelines.

Usage:
    python entrypoints/Conduit/run.py --pipeline documentation [--content "content"]
"""

import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.state.models import ExecutionState, FamilyType
from runtime.artifacts.writer import ArtifactWriter
from entrypoints.Conduit.executors import ConduitExecutor


def run_pipeline(pipeline_id: str, content: str, output_dir: Path):
    """Run a Conduit pipeline."""
    print(f"Running Conduit/{pipeline_id}")
    print(f"Content: {content[:100]}..." if len(content) > 100 else f"Content: {content}")
    print(f"Output: {output_dir}")
    print()
    
    state = ExecutionState(current_family=FamilyType.CONDUIT)
    executor = ConduitExecutor(output_dir)
    writer = ArtifactWriter(output_dir)
    
    context = {
        "content": content or f"Documentation via {pipeline_id}",
        "audience": "technical",
        "format": "markdown",
    }
    
    try:
        if pipeline_id == "documentation":
            state = executor.execute_documentation(state, context)
        elif pipeline_id == "scholarly_writing":
            state = executor.execute_scholarly_writing(state, context)
        elif pipeline_id == "professional_writing":
            state = executor.execute_professional_writing(state, context)
        elif pipeline_id == "handoff_synthesis":
            state = executor.execute_handoff_synthesis(state, context)
        else:
            print(f"ERROR: Unknown pipeline: {pipeline_id}")
            return False
        
        for name, data in state.artifacts.items():
            writer.write_artifact(name, data, pipeline_id, FamilyType.CONDUIT)
        
        print(f"\nPipeline completed successfully")
        print(f"Artifacts produced: {list(state.artifacts.keys())}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Conduit family pipelines")
    parser.add_argument("--pipeline", required=True,
                       choices=["documentation", "scholarly_writing", "professional_writing", "handoff_synthesis"],
                       help="Pipeline to execute")
    parser.add_argument("--content", default="", help="Content to process")
    parser.add_argument("--output", default=str(REPO_ROOT / "runtime_output"), help="Output directory")
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    success = run_pipeline(args.pipeline, args.content, output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
