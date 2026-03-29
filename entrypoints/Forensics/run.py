#!/usr/bin/env python3
"""
Forensics Family Runner - Execute Forensics pipelines.

Usage:
    python entrypoints/Forensics/run.py --pipeline project_mapping [--scope "description"] [--project /path/to/project]
"""

import sys
import argparse
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.state.models import ExecutionState, FamilyType, TrustAssessment
from runtime.artifacts.writer import ArtifactWriter
from entrypoints.Forensics.executors import ForensicsExecutor


def run_pipeline(pipeline_id: str, scope: str, output_dir: Path, project_root: Path):
    """Run a Forensics pipeline."""
    print(f"Running Forensics/{pipeline_id}")
    print(f"Scope: {scope}")
    print(f"Project: {project_root}")
    print(f"Output: {output_dir}")
    print()

    # Initialize
    state = ExecutionState(current_family=FamilyType.FORENSICS)
    executor = ForensicsExecutor(output_dir, project_root=project_root)
    writer = ArtifactWriter(output_dir)

    context = {
        "scope": {
            "description": scope or f"Forensics analysis via {pipeline_id}",
            "boundaries": [],
        },
        "project_root": str(project_root),
    }

    # Execute pipeline
    try:
        if pipeline_id == "project_mapping":
            state = executor.execute_project_mapping(state, context)
        elif pipeline_id == "defragmentation":
            state = executor.execute_defragmentation(state, context)
        elif pipeline_id == "documentation_audit":
            state = executor.execute_documentation_audit(state, context)
        elif pipeline_id == "anomaly_disambiguation":
            state = executor.execute_anomaly_disambiguation(state, context)
        else:
            print(f"ERROR: Unknown pipeline: {pipeline_id}")
            return False

        # Write artifacts
        for name, data in state.artifacts.items():
            writer.write_artifact(name, data, pipeline_id, FamilyType.FORENSICS)

        # Report results
        print(f"\nPipeline completed successfully")
        print(f"Artifacts produced: {list(state.artifacts.keys())}")

        if state.trust_assessment:
            ta = state.trust_assessment
            print(f"\nTrust Assessment:")
            print(f"  Level: {ta.trust_level}")
            print(f"  Entropy: {ta.entropy_level}")
            print(f"  Coherence restored: {ta.coherence_restored}")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Forensics family pipelines")
    parser.add_argument("--pipeline", required=True,
                        choices=["project_mapping", "defragmentation",
                                 "documentation_audit", "anomaly_disambiguation"],
                        help="Pipeline to execute")
    parser.add_argument("--scope", default="", help="Scope description")
    parser.add_argument("--output", default=str(REPO_ROOT / "runtime_output"),
                        help="Output directory")
    parser.add_argument("--project", default=str(Path.cwd()),
                        help="Project root to analyze (defaults to current working directory)")

    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    project_root = Path(args.project).resolve()

    success = run_pipeline(args.pipeline, args.scope, output_dir, project_root)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
