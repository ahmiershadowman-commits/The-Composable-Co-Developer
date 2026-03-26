"""
Tests for transition legality.
"""

import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.registry.loader import SpecRegistry
from runtime.methodology.target_resolver import TargetResolver
from runtime.execution.transitions import TransitionEngine
from runtime.state.models import (
    ExecutionState,
    RouteDecision,
    RouteAction,
    InterventionBand,
    FamilyType,
)


class TestTransitions(unittest.TestCase):
    """Test transition engine."""
    
    def setUp(self):
        registry = SpecRegistry(REPO_ROOT)
        index = registry.load_all()
        resolver = TargetResolver(index)
        self.transitions = TransitionEngine(resolver)
    
    def test_continue_action(self):
        """Test continue action."""
        state = ExecutionState(current_family=FamilyType.FORENSICS)
        decision = RouteDecision(
            action=RouteAction.CONTINUE,
            target="phase:scope",
            intervention_band=InterventionBand.MOTIF,
            reason="test",
            phase_index=0,
        )
        result = self.transitions.execute(decision, state)
        self.assertTrue(result.success)
    
    def test_cross_family_reroute(self):
        """Test cross-family reroute."""
        state = ExecutionState(current_family=FamilyType.FORENSICS)
        decision = RouteDecision(
            action=RouteAction.CROSS_FAMILY_REROUTE,
            target="family:Forge",
            intervention_band=InterventionBand.CROSS_FAMILY_REROUTE,
            reason="test",
            family=FamilyType.FORGE,
        )
        result = self.transitions.execute(decision, state)
        self.assertTrue(result.success)
        self.assertEqual(result.new_state.current_family, FamilyType.FORGE)
    
    def test_sibling_shift(self):
        """Test sibling pipeline shift."""
        state = ExecutionState(current_family=FamilyType.FORENSICS)
        decision = RouteDecision(
            action=RouteAction.SIBLING_SHIFT,
            target="pipeline:Forensics/defragmentation",
            intervention_band=InterventionBand.SIBLING_PIPELINE_SHIFT,
            reason="test",
            pipeline_id="defragmentation",
            family=FamilyType.FORENSICS,
        )
        result = self.transitions.execute(decision, state)
        self.assertTrue(result.success)
        self.assertEqual(result.new_state.current_pipeline, "defragmentation")
    
    def test_forensics_reset(self):
        """Test forensics reset."""
        state = ExecutionState(current_family=FamilyType.FORGE)
        decision = RouteDecision(
            action=RouteAction.FORENSICS_RESET,
            target="forensics_reset",
            intervention_band=InterventionBand.FORENSICS_RESET,
            reason="trust collapse",
        )
        result = self.transitions.execute(decision, state)
        self.assertTrue(result.success)
        self.assertEqual(result.new_state.current_family, FamilyType.FORENSICS)


if __name__ == "__main__":
    unittest.main()
