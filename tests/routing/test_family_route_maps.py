from __future__ import annotations
import unittest
from tests._util import family_route_maps, load_yaml, inventory

class TestFamilyRouteMaps(unittest.TestCase):
    def test_route_maps_match_inventory(self):
        inv = inventory()
        failures = []
        for f in family_route_maps():
            data = load_yaml(f)
            fam = data['family']
            listed = [x['id'] for x in data.get('pipelines',[])]
            experimental = [x['id'] for x in data.get('experimental_pipelines',[])]
            actual = inv.get(fam, [])
            missing = sorted(set(actual) - set(listed) - set(experimental))
            extra = sorted((set(listed) | set(experimental)) - set(actual))
            if missing or extra:
                failures.append({
                    'file': str(f),
                    'missing': missing,
                    'extra': extra,
                })
        self.assertEqual([], failures, f"Route map inventory mismatches: {failures}")

if __name__ == '__main__':
    unittest.main()
