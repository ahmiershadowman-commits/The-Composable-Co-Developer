"""
Motif layer for pattern detection and attention conditioning.

Motifs operate at the inference layer, shaping how the model interprets context
rather than what actions it takes. They are pattern detectors that influence
attention without dictating actions.

See: docs/architecture/motif_layer_rationale.md
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from runtime.state.models import ExecutionState


@dataclass
class MotifSignal:
    """
    Signal from motif pattern detection.
    
    Attributes:
        motif_id: Motif identifier
        detected: Whether pattern was detected
        confidence: Detection confidence (0-1)
        context: Detection context
        suggested_interventions: Related interventions (not triggers)
    """
    motif_id: str
    detected: bool = False
    confidence: float = 0.0
    context: Dict[str, Any] = field(default_factory=dict)
    suggested_interventions: List[str] = field(default_factory=list)


class MotifLayer:
    """
    Motif layer for pattern detection.
    
    Motifs are loaded from YAML files and provide semantic conditioning
    that influences attention without dictating actions.
    """
    
    def __init__(self, motifs_dir: Path):
        self.motifs_dir = motifs_dir
        self._motifs: Dict[str, Dict[str, Any]] = {}
        self._load_motifs()
    
    def _load_motifs(self) -> None:
        """Load all motif definitions from YAML files."""
        if not self.motifs_dir.exists():
            return
        
        for motif_file in self.motifs_dir.glob("*.yaml"):
            if motif_file.name == "registry.yaml":
                continue
            
            data = yaml.safe_load(motif_file.read_text())
            motif_id = data.get("id", motif_file.stem)
            self._motifs[motif_id] = data
    
    def get_motif(self, motif_id: str) -> Optional[Dict[str, Any]]:
        """Get motif definition by ID."""
        return self._motifs.get(motif_id)
    
    def list_motifs(self) -> List[str]:
        """List all loaded motif IDs."""
        return list(self._motifs.keys())
    
    def detect_patterns(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
        active_motifs: Optional[List[str]] = None,
    ) -> List[MotifSignal]:
        """
        Detect motif patterns in current state/context.
        
        This is a placeholder for actual pattern detection.
        In a full implementation, this would analyze the context
        for semantic patterns.
        
        Args:
            state: Current execution state
            context: Current context
            active_motifs: Specific motifs to check (or all)
            
        Returns:
            List of motif signals
        """
        signals = []
        
        motifs_to_check = active_motifs or list(self._motifs.keys())
        
        for motif_id in motifs_to_check:
            motif = self._motifs.get(motif_id)
            if not motif:
                continue
            
            signal = self._detect_motif_pattern(motif_id, motif, state, context)
            signals.append(signal)
        
        return signals
    
    def _detect_motif_pattern(
        self,
        motif_id: str,
        motif: Dict[str, Any],
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> MotifSignal:
        """
        Detect if a motif pattern is present.
        
        This is a simplified implementation. A full implementation
        would use LLM-based pattern detection.
        """
        # Placeholder detection logic
        # In production, this would analyze context for semantic patterns
        
        signal = MotifSignal(
            motif_id=motif_id,
            detected=False,
            confidence=0.0,
            suggested_interventions=motif.get("related_interventions", []),
        )
        
        # Simple heuristic detection based on state
        if motif_id == "unfinished-proof":
            # Detect reasoning gaps
            if state.unresolveds:
                signal.detected = True
                signal.confidence = 0.7
                signal.context = {"unresolved_count": len(state.unresolveds)}
        
        elif motif_id == "watershed":
            # Detect high-stakes decisions
            if "decision" in context.get("problem", "").lower():
                signal.detected = True
                signal.confidence = 0.5
                signal.context = {"decision_context": True}
        
        elif motif_id == "tension_point":
            # Detect conflicts
            if state.trust_assessment and state.trust_assessment.discrepancy_count > 0:
                signal.detected = True
                signal.confidence = min(0.9, 0.3 * state.trust_assessment.discrepancy_count)
                signal.context = {"discrepancy_count": state.trust_assessment.discrepancy_count}
        
        elif motif_id == "absence_signal":
            # Detect missing expected content
            if not state.artifacts:
                signal.detected = True
                signal.confidence = 0.6
                signal.context = {"missing_artifacts": True}
        
        return signal
    
    def get_conditioning_text(self, motif_ids: List[str]) -> str:
        """
        Get conditioning text for motifs to include in context.
        
        This text is added to the LLM context to influence attention.
        """
        conditioning_parts = []
        
        for motif_id in motif_ids:
            motif = self._motifs.get(motif_id)
            if not motif:
                continue
            
            conditioning_parts.append(
                f"## Motif: {motif.get('id', motif_id)}\n"
                f"Pattern: {motif.get('pattern_description', 'N/A')}\n"
                f"Consider: {motif.get('considerations', 'N/A')}"
            )
        
        return "\n\n".join(conditioning_parts) if conditioning_parts else ""
