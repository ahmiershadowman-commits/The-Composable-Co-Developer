from __future__ import annotations
import unittest
from pathlib import Path
from tests._util import REPO_ROOT

TRACE_PATH = REPO_ROOT / 'examples/worked_traces/forensics_defragmentation_forge_trace.md'

class TestWorkedTraceAssertions(unittest.TestCase):
    def test_worked_trace_exists(self):
        self.assertTrue(TRACE_PATH.exists(), 'worked trace file missing')

    def test_worked_trace_contains_expected_progression(self):
        text = TRACE_PATH.read_text(encoding='utf-8')
        required_fragments = [
            'Forensics/project_mapping',
            'Forensics/defragmentation',
            'family:Forge',
            'Forge/coding',
            'Forge/testing',
            'established truth',
            'restored coherence',
        ]
        missing = [frag for frag in required_fragments if frag not in text]
        self.assertEqual([], missing, f"Worked trace missing expected fragments: {missing}")

if __name__ == '__main__':
    unittest.main()
