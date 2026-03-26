"""
Tests for registry loading and indexing.
"""

import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runtime.registry.loader import SpecRegistry, SpecIndex


class TestRegistryLoad(unittest.TestCase):
    """Test registry loading."""
    
    def setUp(self):
        self.registry = SpecRegistry(REPO_ROOT)
    
    def test_registry_loads(self):
        """Test that registry loads without errors."""
        index = self.registry.load_all()
        self.assertIsInstance(index, SpecIndex)
    
    def test_families_loaded(self):
        """Test that families are loaded."""
        index = self.registry.load_all()
        self.assertIn("Forensics", index.families)
        self.assertIn("Forge", index.families)
    
    def test_pipelines_loaded(self):
        """Test that pipelines are loaded."""
        index = self.registry.load_all()
        self.assertTrue(len(index.pipelines) > 0)
    
    def test_forensics_pipelines(self):
        """Test Forensics pipelines are loaded."""
        index = self.registry.load_all()
        self.assertIn("Forensics/project_mapping", index.pipelines)
        self.assertIn("Forensics/defragmentation", index.pipelines)
    
    def test_forge_pipelines(self):
        """Test Forge pipelines are loaded."""
        index = self.registry.load_all()
        self.assertIn("Forge/development", index.pipelines)
        self.assertIn("Forge/coding", index.pipelines)
    
    def test_primitives_loaded(self):
        """Test primitives are loaded."""
        index = self.registry.load_all()
        self.assertTrue(len(index.primitives) > 0)
    
    def test_operators_loaded(self):
        """Test operators are loaded."""
        index = self.registry.load_all()
        self.assertTrue(len(index.operators) > 0)
    
    def test_residue_lenses_loaded(self):
        """Test residue lenses are loaded."""
        index = self.registry.load_all()
        self.assertTrue(len(index.residue_lenses) > 0)
    
    def test_validate_passes(self):
        """Test that validation passes."""
        index = self.registry.load_all()
        errors = self.registry.validate()
        self.assertEqual(len(errors), 0, f"Validation errors: {errors}")


if __name__ == "__main__":
    unittest.main()
