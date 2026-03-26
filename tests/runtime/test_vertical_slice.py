"""
Tests for vertical slice execution.
"""

import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.run_vertical_slice import run_vertical_slice


class TestVerticalSlice(unittest.TestCase):
    """Test vertical slice execution."""
    
    def test_vertical_slice_runs(self):
        """Test that vertical slice runs without errors."""
        output_dir = REPO_ROOT / "test_runtime_output"
        success = run_vertical_slice(output_dir)
        self.assertTrue(success, "Vertical slice should complete successfully")


if __name__ == "__main__":
    unittest.main()
