# RELOCATED — this module has moved to runtime/skills_runners/conduit.py
# This stub exists for backwards compatibility only.
from runtime.skills_runners.conduit import *  # noqa: F401, F403

"""
Conduit Skill - Documentation and synthesis.

Invokes the Conduit family runtime for:
- Documentation
- Scholarly writing
- Professional writing
- Handoff synthesis
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_conduit(pipeline: str = "documentation", content: Optional[str] = None) -> dict:
    """
    Run Conduit family pipeline.
    
    Args:
        pipeline: Pipeline to run (documentation, scholarly_writing, professional_writing, handoff_synthesis)
        content: Content to process or synthesize
        
    Returns:
        Dictionary with execution results
    """
    script = REPO_ROOT / "entrypoints" / "Conduit" / "run.py"
    
    cmd = [
        sys.executable,
        str(script),
        "--pipeline", pipeline,
        "--output", str(REPO_ROOT / "runtime_output"),
    ]
    
    if content:
        cmd.extend(["--content", content])
    
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
            "error": "Conduit execution timed out after 10 minutes",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def main():
    """Main entry point for the skill."""
    print("Conduit Skill - Documentation and Synthesis")
    print("=" * 50)
    print()
    print("Available pipelines:")
    print("  - documentation: Create and update documentation")
    print("  - scholarly_writing: Academic and technical writing")
    print("  - professional_writing: Business and professional content")
    print("  - handoff_synthesis: Create handoff materials")
    print()
    print("Usage: Call run_conduit(pipeline, content)")


if __name__ == "__main__":
    main()
