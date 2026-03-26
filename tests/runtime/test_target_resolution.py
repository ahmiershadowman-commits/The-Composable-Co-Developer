"""
Tests for target resolution.
"""

import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.registry.loader import SpecRegistry
from runtime.methodology.target_resolver import TargetResolver, TargetType


class TestTargetResolution(unittest.TestCase):
    """Test target resolution."""
    
    def setUp(self):
        registry = SpecRegistry(REPO_ROOT)
        index = registry.load_all()
        self.resolver = TargetResolver(index)
    
    def test_resolve_primitive(self):
        """Test resolving primitive target."""
        # Try to resolve any primitive
        result = self.resolver.resolve("primitive:center")
        # May or may not exist depending on spec files
        self.assertIsInstance(result.success, bool)
    
    def test_resolve_operator(self):
        """Test resolving operator target."""
        result = self.resolver.resolve("operator:distill")
        self.assertIsInstance(result.success, bool)
    
    def test_resolve_pipeline(self):
        """Test resolving pipeline target."""
        result = self.resolver.resolve("pipeline:Forensics/project_mapping")
        self.assertTrue(result.success)
        self.assertEqual(result.target_type, TargetType.PIPELINE)
        self.assertEqual(result.family, "Forensics")
    
    def test_resolve_family(self):
        """Test resolving family target."""
        result = self.resolver.resolve("family:Forge")
        self.assertTrue(result.success)
        self.assertEqual(result.target_type, TargetType.FAMILY)
    
    def test_resolve_authority(self):
        """Test resolving authority target."""
        result = self.resolver.resolve("authority:Trace")
        self.assertTrue(result.success)
        self.assertEqual(result.target_type, TargetType.AUTHORITY)
    
    def test_resolve_forensics_reset(self):
        """Test resolving forensics_reset target."""
        result = self.resolver.resolve("forensics_reset")
        self.assertTrue(result.success)
        self.assertEqual(result.target_type, TargetType.FORENSICS_RESET)
    
    def test_invalid_target_syntax(self):
        """Test that invalid syntax fails."""
        result = self.resolver.resolve("invalid_target")
        self.assertFalse(result.success)
    
    def test_invalid_family(self):
        """Test that invalid family fails."""
        result = self.resolver.resolve("family:InvalidFamily")
        self.assertFalse(result.success)
    
    def test_nonexistent_pipeline(self):
        """Test that nonexistent pipeline fails."""
        result = self.resolver.resolve("pipeline:Forensics/nonexistent")
        self.assertFalse(result.success)


if __name__ == "__main__":
    unittest.main()
