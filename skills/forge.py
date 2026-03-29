# RELOCATED — this module has moved to runtime/skills_runners/forge.py
# This stub exists for backwards compatibility only.
from runtime.skills_runners.forge import *  # noqa: F401, F403

"""
Forge Skill - Build/change work.

Invokes the Forge family runtime for:
- Development planning
- Coding implementation
- Testing
- Refactoring
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_forge(pipeline: str = "development", problem: Optional[str] = None) -> dict:
    """
    Run Forge family pipeline.
    
    Args:
        pipeline: Pipeline to run (development, coding, testing, refactor)
        problem: Problem description or change request
        
    Returns:
        Dictionary with execution results
    """
    script = REPO_ROOT / "entrypoints" / "Forge" / "run.py"
    
    cmd = [
        sys.executable,
        str(script),
        "--pipeline", pipeline,
        "--output", str(REPO_ROOT / "runtime_output"),
    ]
    
    if problem:
        cmd.extend(["--problem", problem])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for build work
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
            "error": "Forge execution timed out after 10 minutes",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def main():
    """Main entry point for the skill."""
    print("Forge Skill - Build/Change Work")
    print("=" * 50)
    print()
    print("Available pipelines:")
    print("  - development: Plan and architect build work")
    print("  - coding: Implement code changes")
    print("  - testing: Create and run tests")
    print("  - refactor: Restructure existing code")
    print()
    print("Usage: Call run_forge(pipeline, problem)")


if __name__ == "__main__":
    main()
