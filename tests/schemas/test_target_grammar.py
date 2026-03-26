from __future__ import annotations
import unittest
from tests._util import all_yaml_files, load_yaml, collect_targets, TARGET_PATTERN, primitive_ids, operator_ids, evaluator_ids, inventory

class TestTargetGrammar(unittest.TestCase):
    def test_all_targets_have_valid_syntax_and_resolve(self):
        failures = []
        inv = inventory()
        pipeline_inventory = {f"{fam}/{pid}" for fam, ids in inv.items() for pid in ids}
        families = set(inv.keys())
        authorities = {'Trace','Lever','Residue'}
        primitives = primitive_ids()
        operators = operator_ids()
        evaluators = evaluator_ids()

        for f in all_yaml_files():
            data = load_yaml(f)
            for target in collect_targets(data):
                if not TARGET_PATTERN.match(target):
                    failures.append((str(f), target, 'bad_syntax'))
                    continue
                if target.startswith('primitive:') and target.split(':',1)[1] not in primitives:
                    failures.append((str(f), target, 'missing_primitive'))
                elif target.startswith('operator:') and target.split(':',1)[1] not in operators:
                    failures.append((str(f), target, 'missing_operator'))
                elif target.startswith('evaluator:') and target.split(':',1)[1] not in evaluators:
                    failures.append((str(f), target, 'missing_evaluator'))
                elif target.startswith('pipeline:') and target.split(':',1)[1] not in pipeline_inventory:
                    failures.append((str(f), target, 'missing_pipeline'))
                elif target.startswith('family:') and target.split(':',1)[1] not in families:
                    failures.append((str(f), target, 'missing_family'))
                elif target.startswith('authority:') and target.split(':',1)[1] not in authorities:
                    failures.append((str(f), target, 'missing_authority'))
        self.assertEqual([], failures, f"Target failures: {failures}")

if __name__ == '__main__':
    unittest.main()
