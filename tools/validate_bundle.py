from __future__ import annotations
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    """Run bundle validation using pytest."""
    market_result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "validate_marketplace.py")],
        cwd=str(REPO_ROOT)
    )
    if market_result.returncode != 0:
        return market_result.returncode

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(REPO_ROOT / "tests"), "-v", "--tb=short"],
        cwd=str(REPO_ROOT)
    )
    return result.returncode

if __name__ == '__main__':
    raise SystemExit(main())
