"""
Spec registry for the composable co-developer.

Loads and indexes all specification files:
- Family route maps
- Pipeline specs
- Selectors
- Primitives, operators, evaluators
- Residue lenses
- Feedback loops
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class SpecIndex:
    """Index of all loaded specs."""
    families: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    pipelines: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    selectors: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    primitives: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    operators: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    evaluators: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    residue_lenses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    feedback_loops: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    route_maps: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def get_pipeline(self, family: str, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get a pipeline spec by family and id."""
        key = f"{family}/{pipeline_id}"
        return self.pipelines.get(key)
    
    def get_family_pipelines(self, family: str) -> List[str]:
        """Get all pipeline ids for a family."""
        return [
            k.split("/")[1] 
            for k in self.pipelines.keys() 
            if k.startswith(f"{family}/")
        ]
    
    def has_pipeline(self, family: str, pipeline_id: str) -> bool:
        """Check if a pipeline exists."""
        return f"{family}/{pipeline_id}" in self.pipelines


class SpecRegistry:
    """
    Registry for loading and indexing marketplace specs.
    
    Discovers and loads all YAML specification files,
    building an index for runtime access.
    """
    
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.index = SpecIndex()
        self._loaded = False
    
    def load_all(self) -> SpecIndex:
        """Load and index all specs."""
        if self._loaded:
            return self.index
        
        self._load_primitives()
        self._load_operators()
        self._load_residue()
        self._load_lever()
        self._load_trace()
        self._load_family_route_maps()
        self._load_pipelines()
        self._load_selectors()
        self._load_feedback_loops()
        
        self._loaded = True
        return self.index
    
    def _load_yaml(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load a YAML file."""
        if not path.exists():
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return None
    
    def _load_primitives(self) -> None:
        """Load primitive specs."""
        primitives_dir = self.repo_root / "shared" / "primitives"
        if not primitives_dir.exists():
            return
        
        # Load registry
        registry_path = primitives_dir / "registry.yaml"
        if registry_path.exists():
            data = self._load_yaml(registry_path)
            if data:
                # Index metacognitive primitives
                for subdir in ["metacognitive", "reasoning"]:
                    subdir_path = primitives_dir / subdir
                    if subdir_path.exists():
                        for yaml_file in subdir_path.glob("*.yaml"):
                            spec = self._load_yaml(yaml_file)
                            if spec and "id" in spec:
                                self.index.primitives[spec["id"]] = {
                                    "spec": spec,
                                    "category": subdir,
                                    "path": str(yaml_file),
                                }
    
    def _load_operators(self) -> None:
        """Load operator specs."""
        operators_dir = self.repo_root / "shared" / "operators"
        if not operators_dir.exists():
            return
        
        for yaml_file in operators_dir.glob("*.yaml"):
            spec = self._load_yaml(yaml_file)
            if spec and "id" in spec:
                self.index.operators[spec["id"]] = {
                    "spec": spec,
                    "path": str(yaml_file),
                }
    
    def _load_residue(self) -> None:
        """Load residue lens specs."""
        residue_dir = self.repo_root / "shared" / "Residue"
        if not residue_dir.exists():
            return
        
        # Load registry
        registry_path = residue_dir / "registry.yaml"
        if registry_path.exists():
            data = self._load_yaml(registry_path)
            if data and "lenses" in data:
                for lens_id in data["lenses"]:
                    lens_path = residue_dir / f"{lens_id}.yaml"
                    spec = self._load_yaml(lens_path)
                    if spec:
                        self.index.residue_lenses[lens_id] = {
                            "spec": spec,
                            "path": str(lens_path),
                        }
    
    def _load_lever(self) -> None:
        """Load Lever specs."""
        lever_dir = self.repo_root / "shared" / "Lever"
        if not lever_dir.exists():
            return
        
        for yaml_file in lever_dir.glob("*.yaml"):
            spec = self._load_yaml(yaml_file)
            if spec and "id" in spec:
                self.index.evaluators[spec["id"]] = {
                    "spec": spec,
                    "path": str(yaml_file),
                }
    
    def _load_trace(self) -> None:
        """Load Trace specs."""
        trace_dir = self.repo_root / "shared" / "Trace"
        if not trace_dir.exists():
            return
        
        for yaml_file in trace_dir.glob("*.yaml"):
            spec = self._load_yaml(yaml_file)
            if spec and "id" in spec:
                self.index.evaluators[spec["id"]] = {
                    "spec": spec,
                    "path": str(yaml_file),
                }
    
    def _load_family_route_maps(self) -> None:
        """Load family route maps."""
        entrypoints_dir = self.repo_root / "entrypoints"
        if not entrypoints_dir.exists():
            return
        
        for family_dir in entrypoints_dir.iterdir():
            if not family_dir.is_dir():
                continue
            
            route_map_path = family_dir / "family_route_map.yaml"
            spec = self._load_yaml(route_map_path)
            if spec and "family" in spec:
                family_name = spec["family"]
                self.index.route_maps[family_name] = spec
                self.index.families[family_name] = {
                    "route_map": spec,
                    "path": str(route_map_path),
                }
    
    def _load_pipelines(self) -> None:
        """Load pipeline specs."""
        entrypoints_dir = self.repo_root / "entrypoints"
        if not entrypoints_dir.exists():
            return
        
        for family_dir in entrypoints_dir.iterdir():
            if not family_dir.is_dir():
                continue
            
            pipelines_dir = family_dir / "pipelines"
            if not pipelines_dir.exists():
                continue
            
            for pipeline_dir in pipelines_dir.iterdir():
                if not pipeline_dir.is_dir():
                    continue
                
                pipeline_spec_path = pipeline_dir / "pipeline.yaml"
                spec = self._load_yaml(pipeline_spec_path)
                if spec and "id" in spec and "family" in spec:
                    key = f"{spec['family']}/{spec['id']}"
                    self.index.pipelines[key] = {
                        "spec": spec,
                        "path": str(pipeline_spec_path),
                    }
    
    def _load_selectors(self) -> None:
        """Load selector specs."""
        entrypoints_dir = self.repo_root / "entrypoints"
        if not entrypoints_dir.exists():
            return
        
        for family_dir in entrypoints_dir.iterdir():
            if not family_dir.is_dir():
                continue
            
            selector_path = family_dir / "selector.route.yaml"
            spec = self._load_yaml(selector_path)
            if spec:
                family_name = family_dir.name
                self.index.selectors[family_name] = {
                    "spec": spec,
                    "path": str(selector_path),
                }
    
    def _load_feedback_loops(self) -> None:
        """Load feedback loop specs."""
        loops_dir = self.repo_root / "shared" / "feedback_loops"
        if not loops_dir.exists():
            return
        
        for yaml_file in loops_dir.glob("*.yaml"):
            spec = self._load_yaml(yaml_file)
            if spec and "id" in spec:
                self.index.feedback_loops[spec["id"]] = {
                    "spec": spec,
                    "path": str(yaml_file),
                }
    
    def validate(self) -> List[str]:
        """
        Validate registry consistency.
        
        Returns list of validation errors.
        """
        errors = []
        
        # Check that all pipelines in route maps exist
        for family_name, route_map in self.index.route_maps.items():
            for pipeline in route_map.get("pipelines", []):
                pipeline_id = pipeline.get("id")
                if pipeline_id:
                    key = f"{family_name}/{pipeline_id}"
                    if key not in self.index.pipelines:
                        errors.append(f"Pipeline {key} in route map but not found")
        
        return errors
