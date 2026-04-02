"""
Trace selector for smallest-sufficient intervention.

Trace evaluates state and chooses the minimal intervention
needed to make progress.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from runtime.state.models import (
    ExecutionState,
    RouteDecision,
    RouteAction,
    InterventionBand,
    FamilyType,
    TrustAssessment,
)
from runtime.registry.loader import SpecIndex
from runtime.methodology.target_resolver import TargetResolver


class TraceSelector:
    """
    Metacognitive controller that selects interventions.
    
    Evaluates current state and chooses the smallest
    sufficient intervention to make progress.
    """
    
    def __init__(self, index: SpecIndex, resolver: TargetResolver):
        self.index = index
        self.resolver = resolver
        self._load_trace_specs()
    
    def _load_trace_specs(self) -> None:
        """Load Trace specification files."""
        trace_dir = Path(__file__).parent.parent.parent / "shared" / "Trace"
        self.rubric = None
        self.checklist = None
        self.trigger_glossary = None
        
        rubric_path = trace_dir / "rubric.yaml"
        if rubric_path.exists():
            import yaml
            with open(rubric_path, 'r') as f:
                self.rubric = yaml.safe_load(f)
        
        checklist_path = trace_dir / "checklist.yaml"
        if checklist_path.exists():
            import yaml
            with open(checklist_path, 'r') as f:
                self.checklist = yaml.safe_load(f)
        
        trigger_path = trace_dir / "trigger_glossary.yaml"
        if trigger_path.exists():
            import yaml
            with open(trigger_path, 'r') as f:
                self.trigger_glossary = yaml.safe_load(f)
    
    def evaluate(
        self,
        state: ExecutionState,
        trust: TrustAssessment,
        current_pipeline: Optional[Dict[str, Any]] = None,
    ) -> RouteDecision:
        """
        Evaluate state and return routing decision.
        
        Applies smallest-sufficient intervention principle.
        """
        # Check for trust collapse first
        if trust.should_reroute_to_forensics():
            return RouteDecision(
                action=RouteAction.CROSS_FAMILY_REROUTE,
                target="family:Forensics",
                intervention_band=InterventionBand.CROSS_FAMILY_REROUTE,
                reason="Trust collapse detected",
                family=FamilyType.FORENSICS,
                residue_to_preserve=state.residue_preserved,
            )
        
        # Check for defragmentation need
        if trust.should_reroute_to_defragmentation():
            return RouteDecision(
                action=RouteAction.SIBLING_SHIFT,
                target="pipeline:Forensics/defragmentation",
                intervention_band=InterventionBand.SIBLING_PIPELINE_SHIFT,
                reason="High entropy detected - coherence restoration needed",
                pipeline_id="defragmentation",
                family=FamilyType.FORENSICS,
                residue_to_preserve=state.residue_preserved,
            )
        
        # Check phase progression
        if current_pipeline and "phase_order" in current_pipeline:
            phase_order = current_pipeline.get("phase_order", [])
            if state.phase_index < len(phase_order):
                # Continue in current pipeline
                return RouteDecision(
                    action=RouteAction.CONTINUE,
                    target=f"phase:{phase_order[state.phase_index]}",
                    intervention_band=InterventionBand.MOTIF,
                    reason="Continuing in current phase",
                    phase_index=state.phase_index,
                )
            elif state.phase_index >= len(phase_order):
                # Pipeline complete - check exit conditions
                return self._evaluate_exit(state, current_pipeline)
        
        # Default: continue current work
        return RouteDecision(
            action=RouteAction.CONTINUE,
            target=f"family:{state.current_family.value}",
            intervention_band=InterventionBand.MOTIF,
            reason="No intervention needed - continuing current work",
        )
    
    def _evaluate_exit(
        self,
        state: ExecutionState,
        pipeline: Dict[str, Any],
    ) -> RouteDecision:
        """Evaluate exit conditions and recommend next step."""
        # Check for route recommendation in artifacts
        if "route_recommendation" in state.artifacts:
            recommendation = state.artifacts["route_recommendation"]
            if isinstance(recommendation, dict):
                target = recommendation.get("target")
                if target:
                    return RouteDecision(
                        action=RouteAction.CROSS_FAMILY_REROUTE,
                        target=target,
                        intervention_band=InterventionBand.CROSS_FAMILY_REROUTE,
                        reason="Route recommendation from pipeline exit",
                        residue_to_preserve=state.residue_preserved,
                    )
        
        # Default: return to Forensics for recheck
        return RouteDecision(
            action=RouteAction.CROSS_FAMILY_REROUTE,
            target="family:Forensics",
            intervention_band=InterventionBand.CROSS_FAMILY_REROUTE,
            reason="Pipeline complete - recheck with Forensics",
            family=FamilyType.FORENSICS,
            residue_to_preserve=state.residue_preserved,
        )
    
    def smallest_intervention(
        self,
        trigger: str,
        context: Dict[str, Any],
    ) -> RouteDecision:
        """
        Return smallest intervention for a given trigger.
        
        Used for pivot conditions within pipelines.
        """
        # Check trigger glossary
        if self.trigger_glossary and trigger in self.trigger_glossary.get("triggers", {}):
            trigger_spec = self.trigger_glossary["triggers"][trigger]
            recommended = trigger_spec.get("smallest_response")
            if recommended:
                resolution = self.resolver.resolve(recommended)
                if resolution.success:
                    return RouteDecision(
                        action=RouteAction.CONTINUE,
                        target=recommended,
                        intervention_band=InterventionBand.PRIMITIVE,
                        reason=f"Trigger: {trigger}",
                    )
        
        # Default to selector self-check
        return RouteDecision(
            action=RouteAction.CONTINUE,
            target="authority:Trace",
            intervention_band=InterventionBand.SELECTOR_SELF_CHECK,
            reason=f"Unknown trigger: {trigger} - self-check recommended",
        )
