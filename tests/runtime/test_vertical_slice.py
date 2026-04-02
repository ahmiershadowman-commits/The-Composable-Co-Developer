import os
import unittest
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.run_vertical_slice import run_vertical_slice


class TestVerticalSlice(unittest.TestCase):
    """Test vertical slice execution."""
    
    @pytest.mark.skipif(
        os.environ.get("RUN_VERTICAL_SLICE") != "1",
        reason="Set RUN_VERTICAL_SLICE=1 to run the full vertical slice",
    )
    def test_vertical_slice_runs(self):
        """Test that vertical slice runs without errors."""
        output_dir = REPO_ROOT / "test_runtime_output"
        success = run_vertical_slice(output_dir)
        self.assertTrue(success, "Vertical slice should complete successfully")


if __name__ == "__main__":
    unittest.main()
