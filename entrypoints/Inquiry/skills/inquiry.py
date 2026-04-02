# RELOCATED — this module has moved to runtime/skills_runners/inquiry.py
# This stub exists for backwards compatibility only.
from runtime.skills_runners.inquiry import *  # noqa: F401, F403

"""
Inquiry Skill - Investigation and explanation.

Invokes the Inquiry family runtime for:
- Research
- Hypothesis generation
- Data analysis
- Formalization
- Mathematics
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_inquiry(pipeline: str = "research", question: Optional[str] = None) -> dict:
    """
    Run Inquiry family pipeline.
    
    Args:
        pipeline: Pipeline to run (research, hypothesis_generation, data_analysis, formalization, mathematics)
        question: Research question or investigation target
        
    Returns:
        Dictionary with execution results
    """
    script = REPO_ROOT / "entrypoints" / "Inquiry" / "run.py"
    
    cmd = [
        sys.executable,
        str(script),
        "--pipeline", pipeline,
        "--output", str(REPO_ROOT / "runtime_output"),
    ]
    
    if question:
        cmd.extend(["--question", question])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_dir": str(REPO_ROOT / "runtime_output"),
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Inquiry execution timed out after 10 minutes",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def main():
    """Main entry point for the skill."""
    print("Inquiry Skill - Investigation and Explanation")
    print("=" * 50)
    print()
    print("Available pipelines:")
    print("  - research: Investigate and gather information")
    print("  - hypothesis_generation: Generate testable hypotheses")
    print("  - data_analysis: Analyze data and extract insights")
    print("  - formalization: Create formal specifications")
    print("  - mathematics: Mathematical reasoning and proofs")
    print()
    print("Usage: Call run_inquiry(pipeline, question)")


if __name__ == "__main__":
    main()
