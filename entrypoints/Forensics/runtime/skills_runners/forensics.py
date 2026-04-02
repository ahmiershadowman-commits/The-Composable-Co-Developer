"""
Forensics Skill - Ground-truth establishment.

Invokes the Forensics family runtime for:
- Project state mapping
- Defragmentation
- Documentation audit
- Anomaly disambiguation
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

# Get the repository root (parent of skills directory)
REPO_ROOT = Path(__file__).resolve().parent.parent

def run_forensics(pipeline: str = "project_mapping", scope: Optional[str] = None) -> dict:
    """
    Run Forensics family pipeline.
    
    Args:
        pipeline: Pipeline to run (project_mapping, defragmentation, documentation_audit, anomaly_disambiguation)
        scope: Optional scope description
        
    Returns:
        Dictionary with execution results
    """
    # Build the Python command to run forensics
    script = REPO_ROOT / "entrypoints" / "Forensics" / "run.py"
    
    cmd = [
        sys.executable,
        str(script),
        "--pipeline", pipeline,
        "--output", str(REPO_ROOT / "runtime_output"),
    ]
    
    if scope:
        cmd.extend(["--scope", scope])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
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
            "error": "Forensics execution timed out after 5 minutes",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def main():
    """Main entry point for the skill."""
    print("Forensics Skill - Ground-truth Establishment")
    print("=" * 50)
    print()
    print("Available pipelines:")
    print("  - project_mapping: Map project state and identify trust zones")
    print("  - defragmentation: Restore coherence to fragmented state")
    print("  - documentation_audit: Verify documentation accuracy")
    print("  - anomaly_disambiguation: Investigate conflicting signals")
    print()
    print("Usage: Call run_forensics(pipeline, scope)")


if __name__ == "__main__":
    main()
