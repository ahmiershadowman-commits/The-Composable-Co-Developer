from __future__ import annotations
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    suite = unittest.defaultTestLoader.discover(str(REPO_ROOT / 'tests'))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    raise SystemExit(main())
