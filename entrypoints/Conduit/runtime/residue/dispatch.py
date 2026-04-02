"""
Residue dispatch for suspicious-surface investigation.

Residue provides investigative lenses for anomalous signals
and recommends smallest first responses.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

from runtime.state.models import RouteDecision, RouteAction, InterventionBand


@dataclass
class LensRecommendation:
    """Output from residue lens dispatch."""
    lens_id: str
    oddity_preserved: bool
    first_response: Optional[str]
    escalate_to: Optional[str]
    notes: List[str]


class ResidueDispatch:
    """
    Dispatches residue lenses for investigation.
    
    Preserves oddity before forced reroute and recommends
    smallest first response.
    """
    
    def __init__(self):
        self.lenses: Dict[str, Dict[str, Any]] = {}
        self.trigger_map: Dict[str, Any] = {}
        self._load_specs()
    
    def _load_specs(self) -> None:
        """Load residue specification files."""
        import yaml
        
        residue_dir = Path(__file__).parent.parent.parent / "shared" / "Residue"
        
        # Load registry
        registry_path = residue_dir / "registry.yaml"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = yaml.safe_load(f)
                lens_ids = registry.get("lenses", [])
                
                for lens_id in lens_ids:
                    lens_path = residue_dir / f"{lens_id}.yaml"
                    if lens_path.exists():
                        with open(lens_path, 'r') as f:
                            self.lenses[lens_id] = yaml.safe_load(f)
        
        # Load trigger map
        trigger_path = residue_dir / "trigger_map.yaml"
        if trigger_path.exists():
            with open(trigger_path, 'r') as f:
                self.trigger_map = yaml.safe_load(f)
    
    def dispatch(
        self,
        signal: str,
        context: Dict[str, Any],
    ) -> LensRecommendation:
        """
        Dispatch appropriate lens for a suspicious signal.
        
        Returns recommendation for first response.
        """
        # Check trigger map for known signals
        if signal in self.trigger_map.get("triggers", {}):
            trigger_spec = self.trigger_map["triggers"][signal]
            lens_id = trigger_spec.get("lens")
            first_response = trigger_spec.get("first_response")
            escalate_to = trigger_spec.get("escalate_to")
            
            if lens_id and lens_id in self.lenses:
                return LensRecommendation(
                    lens_id=lens_id,
                    oddity_preserved=True,
                    first_response=first_response,
                    escalate_to=escalate_to,
                    notes=[f"Signal matched: {signal}"],
                )
        
        # Try to match signal to lens by type
        lens_id = self._match_signal_to_lens(signal)
        if lens_id:
            return LensRecommendation(
                lens_id=lens_id,
                oddity_preserved=True,
                first_response="investigate",
                escalate_to="authority:Trace",
                notes=[f"Signal matched to lens: {lens_id}"],
            )
        
        # Default: preserve oddity and escalate
        return LensRecommendation(
            lens_id="signal",
            oddity_preserved=True,
            first_response="preserve_and_note",
            escalate_to="authority:Trace",
            notes=[f"Unknown signal: {signal} - preserving for investigation"],
        )
    
    def _match_signal_to_lens(self, signal: str) -> Optional[str]:
        """Match a signal to an appropriate lens."""
        signal_lower = signal.lower()
        
        # Simple keyword matching
        lens_keywords = {
            "misfit": ["mismatch", "doesn't fit", "wrong", "conflict"],
            "absence": ["missing", "absent", "not found", "gap"],
            "tension": ["tension", "conflict", "disagree", "contradiction"],
            "warp": ["distorted", "warped", "twisted", "corrupted"],
            "burden": ["heavy", "complex", "burden", "overloaded"],
            "edge": ["edge", "boundary", "limit", "fringe"],
            "offset": ["offset", "shifted", "displaced", "misaligned"],
            "signal": ["signal", "anomaly", "unusual", "suspicious"],
        }
        
        for lens_id, keywords in lens_keywords.items():
            for keyword in keywords:
                if keyword in signal_lower:
                    return lens_id
        
        return None
    
    def get_lens(self, lens_id: str) -> Optional[Dict[str, Any]]:
        """Get a lens specification by id."""
        return self.lenses.get(lens_id)
    
    def apply_lens(
        self,
        lens_id: str,
        target: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        """
        Apply a lens to a target.
        
        Returns (success, findings).
        """
        lens = self.lenses.get(lens_id)
        if not lens:
            return False, [f"Unknown lens: {lens_id}"]
        
        findings = []
        
        # Apply lens-specific investigation
        lens_type = lens.get("kind", "unknown")
        
        if lens_type == "investigative_lens":
            # Generic lens application
            findings.append(f"Applied {lens_id} lens")
            
            # Check for lens-specific patterns
            if "patterns" in lens:
                for pattern in lens["patterns"]:
                    if self._check_pattern(pattern, target):
                        findings.append(f"Pattern matched: {pattern.get('name', 'unknown')}")
        
        return True, findings
    
    def _check_pattern(
        self,
        pattern: Dict[str, Any],
        target: Dict[str, Any],
    ) -> bool:
        """Check if a pattern matches the target."""
        # Simple pattern matching - can be extended
        pattern_type = pattern.get("type")
        if pattern_type == "absence":
            field = pattern.get("field")
            return field not in target
        
        return False
