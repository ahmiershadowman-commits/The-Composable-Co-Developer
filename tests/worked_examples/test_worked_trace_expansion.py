"""
Tests for worked trace expansion.

Validates that all worked traces exist and contain expected content.
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKED_TRACES_DIR = REPO_ROOT / "examples" / "worked_traces"


class TestInquiryTrace(unittest.TestCase):
    """Test the Inquiry worked trace."""

    def test_inquiry_trace_exists(self):
        """Inquiry trace file should exist."""
        trace_path = WORKED_TRACES_DIR / "inquiry_trace.md"
        self.assertTrue(trace_path.exists(), f"Missing: {trace_path}")

    def test_inquiry_trace_has_forensics_step(self):
        """Inquiry trace should include Forensics step."""
        trace_path = WORKED_TRACES_DIR / "inquiry_trace.md"
        content = trace_path.read_text()
        self.assertIn("Forensics/project_mapping", content)

    def test_inquiry_trace_has_research_step(self):
        """Inquiry trace should include research step."""
        trace_path = WORKED_TRACES_DIR / "inquiry_trace.md"
        content = trace_path.read_text()
        self.assertIn("Inquiry/research", content)

    def test_inquiry_trace_has_route_history(self):
        """Inquiry trace should include route history."""
        trace_path = WORKED_TRACES_DIR / "inquiry_trace.md"
        content = trace_path.read_text()
        self.assertIn("Route History", content)


class TestConduitFallbackTrace(unittest.TestCase):
    """Test the Conduit Fallback worked trace."""

    def test_conduit_fallback_trace_exists(self):
        """Conduit fallback trace file should exist."""
        trace_path = WORKED_TRACES_DIR / "conduit_fallback_trace.md"
        self.assertTrue(trace_path.exists(), f"Missing: {trace_path}")

    def test_conduit_fallback_has_trust_collapse(self):
        """Conduit fallback should include trust collapse."""
        trace_path = WORKED_TRACES_DIR / "conduit_fallback_trace.md"
        content = trace_path.read_text(encoding="utf-8")
        self.assertIn("Trust Collapse", content)

    def test_conduit_fallback_has_defragmentation(self):
        """Conduit fallback should include defragmentation."""
        trace_path = WORKED_TRACES_DIR / "conduit_fallback_trace.md"
        content = trace_path.read_text()
        self.assertIn("Forensics/defragmentation", content)

    def test_conduit_fallback_has_handoff(self):
        """Conduit fallback should include handoff synthesis."""
        trace_path = WORKED_TRACES_DIR / "conduit_fallback_trace.md"
        content = trace_path.read_text()
        self.assertIn("Conduit/handoff_synthesis", content)


class TestAuthorityEscalationTrace(unittest.TestCase):
    """Test the Authority Escalation worked trace."""

    def test_authority_escalation_trace_exists(self):
        """Authority escalation trace file should exist."""
        trace_path = WORKED_TRACES_DIR / "authority_escalation_trace.md"
        self.assertTrue(trace_path.exists(), f"Missing: {trace_path}")

    def test_authority_escalation_has_trace_first(self):
        """Authority escalation should start with Trace."""
        trace_path = WORKED_TRACES_DIR / "authority_escalation_trace.md"
        content = trace_path.read_text(encoding="utf-8")
        self.assertIn("Trace", content)

    def test_authority_escalation_has_residue(self):
        """Authority escalation should include Residue."""
        trace_path = WORKED_TRACES_DIR / "authority_escalation_trace.md"
        content = trace_path.read_text(encoding="utf-8")
        self.assertIn("Residue", content)

    def test_authority_escalation_has_lever(self):
        """Authority escalation should include Lever."""
        trace_path = WORKED_TRACES_DIR / "authority_escalation_trace.md"
        content = trace_path.read_text(encoding="utf-8")
        self.assertIn("Lever", content)

    def test_authority_escalation_order(self):
        """Authority escalation should follow correct order."""
        trace_path = WORKED_TRACES_DIR / "authority_escalation_trace.md"
        content = trace_path.read_text(encoding="utf-8")
        # Trace should come before Lever
        trace_pos = content.find("Trace")
        lever_pos = content.find("Lever")
        self.assertLess(trace_pos, lever_pos, "Trace must come before Lever")


class TestRefactorVsDefragmentationTrace(unittest.TestCase):
    """Test the Refactor vs Defragmentation worked trace."""

    def test_refactor_vs_defrag_trace_exists(self):
        """Refactor vs defragmentation trace file should exist."""
        trace_path = WORKED_TRACES_DIR / "refactor_vs_defragmentation_trace.md"
        self.assertTrue(trace_path.exists(), f"Missing: {trace_path}")

    def test_refactor_vs_defrag_has_refactor_scenario(self):
        """Trace should include refactor scenario."""
        trace_path = WORKED_TRACES_DIR / "refactor_vs_defragmentation_trace.md"
        content = trace_path.read_text()
        self.assertIn("Forge/refactor", content)

    def test_refactor_vs_defrag_has_defrag_scenario(self):
        """Trace should include defragmentation scenario."""
        trace_path = WORKED_TRACES_DIR / "refactor_vs_defragmentation_trace.md"
        content = trace_path.read_text()
        self.assertIn("Forensics/defragmentation", content)

    def test_refactor_vs_defrag_has_decision_boundary(self):
        """Trace should include decision boundary."""
        trace_path = WORKED_TRACES_DIR / "refactor_vs_defragmentation_trace.md"
        content = trace_path.read_text()
        self.assertIn("Decision Boundary", content)


class TestAllWorkedTraces(unittest.TestCase):
    """Test that all required worked traces exist."""

    REQUIRED_TRACES = [
        "forensics_defragmentation_forge_trace.md",
        "inquiry_trace.md",
        "conduit_fallback_trace.md",
        "authority_escalation_trace.md",
        "refactor_vs_defragmentation_trace.md",
    ]

    def test_all_required_traces_exist(self):
        """All required worked traces should exist."""
        missing = []
        for trace_name in self.REQUIRED_TRACES:
            trace_path = WORKED_TRACES_DIR / trace_name
            if not trace_path.exists():
                missing.append(trace_name)

        self.assertEqual(
            [],
            missing,
            f"Missing worked traces: {missing}"
        )


if __name__ == "__main__":
    unittest.main()
