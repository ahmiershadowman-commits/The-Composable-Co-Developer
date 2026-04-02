from __future__ import annotations
import unittest
from tests._util import pipeline_files, load_yaml

REQUIRED_PIPELINE_FIELDS = [
    'id','family','kind','frame_alias','status','purpose','entry_conditions',
    'shared_authorities','phase_order','phase_contracts',
    'smallest_sufficient_interventions','pivot_conditions','exit_conditions','artifacts'
]
DEPRECATED_FIELDS = ['phases','methods','local_methods','triggers','critical_triggers','required_artifacts']

class TestPipelineShape(unittest.TestCase):
    def test_all_pipelines_use_canonical_shape(self):
        failures = []
        for f in pipeline_files():
            data = load_yaml(f)
            missing = [k for k in REQUIRED_PIPELINE_FIELDS if k not in data]
            deprecated = [k for k in DEPRECATED_FIELDS if k in data]
            if missing or deprecated:
                failures.append({
                    'file': str(f),
                    'missing': missing,
                    'deprecated': deprecated,
                })
        self.assertEqual([], failures, f"Pipeline schema failures: {failures}")

if __name__ == '__main__':
    unittest.main()
