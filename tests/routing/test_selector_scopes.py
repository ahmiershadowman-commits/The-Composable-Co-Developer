from __future__ import annotations
import unittest
from pathlib import Path
from tests._util import selector_files, load_yaml, REPO_ROOT

class TestSelectorScopes(unittest.TestCase):
    def test_selector_scopes_match_core_route_map(self):
        failures = []
        for f in selector_files():
            data = load_yaml(f)
            fam = data['family']
            route_map = load_yaml(REPO_ROOT / f'entrypoints/{fam}/family_route_map.yaml')
            core_ids = sorted([x['id'] for x in route_map.get('pipelines', [])])
            scope = sorted(data.get('pipeline_scope', []))
            if scope != core_ids:
                failures.append({
                    'file': str(f),
                    'scope': scope,
                    'core_ids': core_ids,
                })
        self.assertEqual([], failures, f"Selector scope mismatches: {failures}")

if __name__ == '__main__':
    unittest.main()
