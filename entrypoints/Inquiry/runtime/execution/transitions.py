"""
Transition engine for routing across boundaries.

Handles legal transitions between:
- Phases within a pipeline
- Pipelines within a family
- Families (cross-family reroute)
- Authority calls
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

from runtime.state.models import (
    ExecutionState,
    RouteDecision,
    RouteAction,
    FamilyType,
)
from runtime.methodology.target_resolver import TargetResolver, TargetResolution


@dataclass
class TransitionResult:
    """Result of a transition attempt."""
    success: bool
    new_state: ExecutionState
    errors: List[str]
    warnings: List[str]


class TransitionEngine:
    """
    Executes legal transitions between states.
    
    Validates transitions against route maps and target grammar.
    """
    
    def __init__(self, resolver: TargetResolver):
        self.resolver = resolver
    
    def execute(
        self,
        decision: RouteDecision,
        state: ExecutionState,
        pipeline_spec: Optional[Dict[str, Any]] = None,
    ) -> TransitionResult:
        """
        Execute a routing decision.
        
        Returns new state or errors.
        """
        errors = []
        warnings = []
        
        # Create new state copy
        new_state = ExecutionState(
            current_family=state.current_family,
            current_pipeline=state.current_pipeline,
            current_phase=state.current_phase,
            phase_index=state.phase_index,
            artifacts=dict(state.artifacts),
            route_history=list(state.route_history),
            trust_assessment=state.trust_assessment,
            residue_preserved=dict(state.residue_preserved),
            unresolveds=list(state.unresolveds),
            errors=list(state.errors),
            started_at=state.started_at,
        )
        
        # Execute based on action type
        if decision.action == RouteAction.CONTINUE:
            self._execute_continue(decision, new_state, pipeline_spec)
        
        elif decision.action == RouteAction.PHASE_PIVOT:
            self._execute_phase_pivot(decision, new_state, pipeline_spec)
        
        elif decision.action == RouteAction.SIBLING_SHIFT:
            self._execute_sibling_shift(decision, new_state)
        
        elif decision.action == RouteAction.CROSS_FAMILY_REROUTE:
            self._execute_cross_family_reroute(decision, new_state)
        
        elif decision.action == RouteAction.AUTHORITY_CALL:
            self._execute_authority_call(decision, new_state)
        
        elif decision.action == RouteAction.FORENSICS_RESET:
            self._execute_forensics_reset(decision, new_state)
        
        else:
            errors.append(f"Unknown action type: {decision.action}")
        
        # Record decision in history
        if not errors:
            new_state.add_route_decision(decision)
        
        return TransitionResult(
            success=len(errors) == 0,
            new_state=new_state,
            errors=errors,
            warnings=warnings,
        )
    
    def _execute_continue(
        self,
        decision: RouteDecision,
        state: ExecutionState,
        pipeline_spec: Optional[Dict[str, Any]],
    ) -> None:
        """Execute continue action."""
        if decision.phase_index is not None:
            state.phase_index = decision.phase_index
            
            if pipeline_spec and "phase_order" in pipeline_spec:
                phase_order = pipeline_spec.get("phase_order", [])
                if 0 <= decision.phase_index < len(phase_order):
                    state.current_phase = phase_order[decision.phase_index]
    
    def _execute_phase_pivot(
        self,
        decision: RouteDecision,
        state: ExecutionState,
        pipeline_spec: Optional[Dict[str, Any]],
    ) -> None:
        """Execute phase pivot."""
        if decision.phase_index is not None:
            state.phase_index = decision.phase_index
            
            if pipeline_spec and "phase_order" in pipeline_spec:
                phase_order = pipeline_spec.get("phase_order", [])
                if 0 <= decision.phase_index < len(phase_order):
                    state.current_phase = phase_order[decision.phase_index]
    
    def _execute_sibling_shift(
        self,
        decision: RouteDecision,
        state: ExecutionState,
    ) -> None:
        """Execute sibling pipeline shift."""
        if decision.pipeline_id:
            state.current_pipeline = decision.pipeline_id
            state.phase_index = 0  # Reset to first phase
        
        if decision.family:
            state.current_family = decision.family
    
    def _execute_cross_family_reroute(
        self,
        decision: RouteDecision,
        state: ExecutionState,
    ) -> None:
        """Execute cross-family reroute."""
        if decision.family:
            state.current_family = decision.family
            state.current_pipeline = None
            state.current_phase = None
            state.phase_index = 0
        
        # Preserve residue across family boundary
        if decision.residue_to_preserve:
            state.residue_preserved.update(decision.residue_to_preserve)
    
    def _execute_authority_call(
        self,
        decision: RouteDecision,
        state: ExecutionState,
    ) -> None:
        """Execute authority call."""
        # Authority calls don't change state
        # They return structured data for the caller
        pass
    
    def _execute_forensics_reset(
        self,
        decision: RouteDecision,
        state: ExecutionState,
    ) -> None:
        """Execute forensics reset."""
        state.current_family = FamilyType.FORENSICS
        state.current_pipeline = "project_mapping"
        state.current_phase = "scope"
        state.phase_index = 0
        state.trust_assessment = None  # Reset trust assessment
    
    def validate_transition(
        self,
        from_state: ExecutionState,
        to_target: str,
        pipeline_spec: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, List[str]]:
        """
        Validate a transition before executing.
        
        Returns (is_valid, errors).
        """
        errors = []
        
        # Resolve target
        resolution = self.resolver.resolve(to_target)
        if not resolution.success:
            errors.append(f"Invalid target: {resolution.error}")
            return False, errors
        
        # Check phase transitions
        if resolution.target_type.value == "phase":
            if not pipeline_spec:
                errors.append("Pipeline spec required for phase transition")
                return False, errors
            
            phase_order = pipeline_spec.get("phase_order", [])
            current_phase = from_state.phase_index
            
            # Validate phase index is within bounds
            if current_phase >= len(phase_order):
                errors.append("Current phase index out of bounds")
        
        # Check family transitions
        if resolution.target_type.value == "family":
            # Family transitions are always valid if target is valid family
            pass
        
        return len(errors) == 0, errors
