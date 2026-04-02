"""
Canonical target grammar and resolver.

Target grammar defines valid runtime targets:
- primitive:<name>
- operator:<name>
- evaluator:<name>
- method:<name>
- pipeline:<Family>/<pipeline_id>
- family:<Family>
- authority:<Trace|Lever|Residue>
- forensics_reset
"""

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from runtime.registry.loader import SpecIndex


class TargetType(str, Enum):
    """Valid target types."""
    PRIMITIVE = "primitive"
    OPERATOR = "operator"
    EVALUATOR = "evaluator"
    METHOD = "method"
    PIPELINE = "pipeline"
    FAMILY = "family"
    AUTHORITY = "authority"
    FORENSICS_RESET = "forensics_reset"


@dataclass
class TargetResolution:
    """Result of resolving a target string."""
    success: bool
    target_type: Optional[TargetType] = None
    target_id: Optional[str] = None
    family: Optional[str] = None
    spec: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    path: Optional[Path] = None


class TargetResolver:
    """
    Resolves canonical target strings to typed objects.
    
    Validates target syntax and looks up specs in the index.
    """
    
    TARGET_PATTERN = re.compile(
        r'^(primitive:[\w_]+|operator:[\w_]+|evaluator:[\w_]+|method:[\w_]+|'
        r'pipeline:[A-Za-z]+/[\w_]+|family:[A-Za-z]+|authority:(Trace|Lever|Residue)|'
        r'forensics_reset)$'
    )
    
    def __init__(self, index: SpecIndex):
        self.index = index
        self._valid_families = {"Forensics", "Forge", "Inquiry", "Conduit"}
        self._valid_authorities = {"Trace", "Lever", "Residue"}
    
    def resolve(self, target: str) -> TargetResolution:
        """
        Resolve a target string to a typed object.
        
        Returns TargetResolution with success status and spec data.
        """
        # Validate syntax
        if not self.TARGET_PATTERN.match(target):
            return TargetResolution(
                success=False,
                error=f"Invalid target syntax: {target}"
            )
        
        # Parse target
        if target == "forensics_reset":
            return TargetResolution(
                success=True,
                target_type=TargetType.FORENSICS_RESET,
                target_id="forensics_reset"
            )
        
        parts = target.split(":", 1)
        if len(parts) != 2:
            return TargetResolution(
                success=False,
                error=f"Invalid target format: {target}"
            )
        
        target_type_str, target_value = parts
        try:
            target_type = TargetType(target_type_str)
        except ValueError:
            return TargetResolution(
                success=False,
                error=f"Unknown target type: {target_type_str}"
            )
        
        # Resolve based on type
        if target_type == TargetType.PRIMITIVE:
            return self._resolve_primitive(target_value)
        elif target_type == TargetType.OPERATOR:
            return self._resolve_operator(target_value)
        elif target_type == TargetType.EVALUATOR:
            return self._resolve_evaluator(target_value)
        elif target_type == TargetType.METHOD:
            return self._resolve_method(target_value)
        elif target_type == TargetType.PIPELINE:
            return self._resolve_pipeline(target_value)
        elif target_type == TargetType.FAMILY:
            return self._resolve_family(target_value)
        elif target_type == TargetType.AUTHORITY:
            return self._resolve_authority(target_value)
        
        return TargetResolution(
            success=False,
            error=f"Unhandled target type: {target_type}"
        )
    
    def _resolve_primitive(self, name: str) -> TargetResolution:
        """Resolve a primitive target."""
        if name in self.index.primitives:
            spec_data = self.index.primitives[name]
            return TargetResolution(
                success=True,
                target_type=TargetType.PRIMITIVE,
                target_id=name,
                spec=spec_data.get("spec"),
                path=Path(spec_data.get("path", "")) if spec_data.get("path") else None
            )
        return TargetResolution(
            success=False,
            error=f"Primitive not found: {name}"
        )
    
    def _resolve_operator(self, name: str) -> TargetResolution:
        """Resolve an operator target."""
        if name in self.index.operators:
            spec_data = self.index.operators[name]
            return TargetResolution(
                success=True,
                target_type=TargetType.OPERATOR,
                target_id=name,
                spec=spec_data.get("spec"),
                path=Path(spec_data.get("path", "")) if spec_data.get("path") else None
            )
        return TargetResolution(
            success=False,
            error=f"Operator not found: {name}"
        )
    
    def _resolve_evaluator(self, name: str) -> TargetResolution:
        """Resolve an evaluator target."""
        if name in self.index.evaluators:
            spec_data = self.index.evaluators[name]
            return TargetResolution(
                success=True,
                target_type=TargetType.EVALUATOR,
                target_id=name,
                spec=spec_data.get("spec"),
                path=Path(spec_data.get("path", "")) if spec_data.get("path") else None
            )
        return TargetResolution(
            success=False,
            error=f"Evaluator not found: {name}"
        )
    
    def _resolve_method(self, name: str) -> TargetResolution:
        """Resolve a method target."""
        # Methods are defined within pipelines
        # For now, return a placeholder resolution
        return TargetResolution(
            success=True,
            target_type=TargetType.METHOD,
            target_id=name,
            spec={"id": name, "kind": "method"}
        )
    
    def _resolve_pipeline(self, value: str) -> TargetResolution:
        """Resolve a pipeline target."""
        parts = value.split("/", 1)
        if len(parts) != 2:
            return TargetResolution(
                success=False,
                error=f"Invalid pipeline target: {value}"
            )
        
        family, pipeline_id = parts
        
        if family not in self._valid_families:
            return TargetResolution(
                success=False,
                error=f"Invalid family: {family}"
            )
        
        key = f"{family}/{pipeline_id}"
        if key in self.index.pipelines:
            spec_data = self.index.pipelines[key]
            return TargetResolution(
                success=True,
                target_type=TargetType.PIPELINE,
                target_id=pipeline_id,
                family=family,
                spec=spec_data.get("spec"),
                path=Path(spec_data.get("path", "")) if spec_data.get("path") else None
            )
        
        return TargetResolution(
            success=False,
            error=f"Pipeline not found: {key}"
        )
    
    def _resolve_family(self, name: str) -> TargetResolution:
        """Resolve a family target."""
        if name not in self._valid_families:
            return TargetResolution(
                success=False,
                error=f"Invalid family: {name}"
            )
        
        if name in self.index.families:
            spec_data = self.index.families[name]
            return TargetResolution(
                success=True,
                target_type=TargetType.FAMILY,
                target_id=name,
                spec=spec_data.get("route_map"),
                path=Path(spec_data.get("path", "")) if spec_data.get("path") else None
            )
        
        return TargetResolution(
            success=True,
            target_type=TargetType.FAMILY,
            target_id=name,
            spec={"family": name}
        )
    
    def _resolve_authority(self, name: str) -> TargetResolution:
        """Resolve an authority target."""
        if name not in self._valid_authorities:
            return TargetResolution(
                success=False,
                error=f"Invalid authority: {name}"
            )
        
        # Authority specs are in shared/
        authority_dir = Path(__file__).parent.parent.parent / "shared" / name
        if authority_dir.exists():
            return TargetResolution(
                success=True,
                target_type=TargetType.AUTHORITY,
                target_id=name,
                spec={"authority": name, "path": str(authority_dir)}
            )
        
        return TargetResolution(
            success=True,
            target_type=TargetType.AUTHORITY,
            target_id=name,
            spec={"authority": name}
        )
    
    def validate_target(self, target: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a target string.
        
        Returns (is_valid, error_message).
        """
        result = self.resolve(target)
        return result.success, result.error
