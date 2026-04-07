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

# Authority modules — imported lazily inside _execute_authority_call to avoid
# circular-import risk at module load time.
_AUTHORITY_MODULES_LOADED = False


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
    Fires PRE_TRANSITION hooks (e.g., trigger_ownership_hook) before
    executing any authority call, cross-family reroute, or sibling shift.
    """

    def __init__(self, resolver: TargetResolver, hook_registry=None):
        self.resolver = resolver
        # Optional HookRegistry — injected by RuntimeDispatcher so that
        # PRE_TRANSITION hooks (trigger_ownership_hook) are fired before
        # high-impact transitions.  When None, hooks are skipped (tests /
        # lightweight use-sites that don't need enforcement).
        self._hooks = hook_registry

    def execute(
        self,
        decision: RouteDecision,
        state: ExecutionState,
        pipeline_spec: Optional[Dict[str, Any]] = None,
    ) -> TransitionResult:
        """
        Execute a routing decision.

        Fires PRE_TRANSITION hooks before high-impact transitions so that
        the trigger ownership model can block violations before they reach
        the state mutation layer.

        Returns new state or errors.
        """
        errors = []
        warnings = []

        # Fire PRE_TRANSITION hooks for transitions that need ownership validation
        _PRE_TRANSITION_ACTIONS = {
            RouteAction.AUTHORITY_CALL,
            RouteAction.CROSS_FAMILY_REROUTE,
            RouteAction.SIBLING_SHIFT,
            RouteAction.FORENSICS_RESET,
        }
        if self._hooks is not None and decision.action in _PRE_TRANSITION_ACTIONS:
            hook_result = self._fire_pre_transition(decision, state)
            if not hook_result.continue_execution:
                errors.append(hook_result.error_message or "PRE_TRANSITION hook blocked transition")
                return TransitionResult(
                    success=False,
                    new_state=state,
                    errors=errors,
                    warnings=warnings,
                )

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

    def _fire_pre_transition(self, decision: RouteDecision, state: ExecutionState):
        """Build a HookContext and fire PRE_TRANSITION hooks."""
        from hooks.context import HookContext
        from hooks.registry import HookEvent

        # Populate the context keys that trigger_ownership_hook reads
        hook_context_data = {
            "pending_action": decision.action.value,
            "pending_target": decision.target,
            "pending_trigger": getattr(decision, "trigger", ""),
            "pending_authority_data": decision.authority_data or {},
        }

        hc = HookContext(
            session_id=f"{state.current_family.value}/{state.current_pipeline or ''}",
            pipeline_id=f"{state.current_family.value}/{state.current_pipeline or ''}",
            phase_id=state.current_phase,
            state=state,
            context=hook_context_data,
        )
        return self._hooks.execute(HookEvent.PRE_TRANSITION, hc)
    
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
        """Dispatch to Trace, Lever, or Residue authority and record results.

        Target format: "authority:Trace" | "authority:Lever" | "authority:Residue"
        authority_data carries any extra payload the caller attached.
        """
        target = decision.target or ""
        authority_data = decision.authority_data or {}
        authority_name = target.split(":", 1)[-1] if ":" in target else target

        if authority_name == "Trace":
            self._call_trace(state, authority_data)
        elif authority_name == "Lever":
            self._call_lever(state, authority_data)
        elif authority_name == "Residue":
            self._call_residue(state, authority_data)
        else:
            state.errors.append(
                f"Unknown authority target: '{target}' — "
                "expected authority:Trace, authority:Lever, or authority:Residue"
            )

    def _call_trace(self, state: ExecutionState, data: Dict[str, Any]) -> None:
        """Invoke TraceSelector and record its decision in state artifacts."""
        from runtime.trace.selector import TraceSelector
        from runtime.state.models import TrustAssessment
        from runtime.methodology.spec_index import SpecIndex

        spec_index = getattr(self, "_spec_index", None)
        if spec_index is None:
            spec_index = SpecIndex()
            self._spec_index = spec_index  # cache

        selector = TraceSelector(spec_index, self.resolver)

        # Use existing trust assessment or build a neutral default
        trust = state.trust_assessment or TrustAssessment(trust_level="medium")
        pipeline_spec = data.get("pipeline_spec")
        decision = selector.evaluate(state, trust, pipeline_spec)

        trigger = data.get("trigger", "authority_call")
        context = data.get("context", dict(state.artifacts))
        intervention = selector.smallest_intervention(trigger, context)

        state.add_artifact("_authority_trace_evaluation", {
            "decision_action": decision.action.value if decision else None,
            "decision_target": decision.target if decision else None,
            "decision_reason": decision.reason if decision else None,
            "intervention": intervention.to_dict() if hasattr(intervention, "to_dict") else str(intervention),
            "invoked_at": __import__("datetime").datetime.now().isoformat(),
        })

    def _call_lever(self, state: ExecutionState, data: Dict[str, Any]) -> None:
        """Invoke LeverEscalation for the evaluator named in authority_data."""
        from runtime.lever.escalation import LeverEscalation

        lever = LeverEscalation()
        evaluator_id = data.get("evaluator_id", "trust_evaluator")
        context = data.get("context", dict(state.artifacts))

        result = lever.evaluate(evaluator_id, context)

        state.add_artifact("_authority_lever_result", {
            "evaluator_id": result.evaluator_id,
            "success": result.success,
            "findings": result.findings,
            "recommendation": result.recommendation,
            "commitment_level": result.commitment_level,
            "reopen_conditions": result.reopen_conditions,
            "invoked_at": __import__("datetime").datetime.now().isoformat(),
        })

    def _call_residue(self, state: ExecutionState, data: Dict[str, Any]) -> None:
        """Invoke ResidueDispatch for a surface signal and record lens recommendation."""
        from runtime.residue.dispatch import ResidueDispatch

        dispatch = ResidueDispatch()
        signal = data.get("signal", "anomaly_detected")
        context = data.get("context", dict(state.artifacts))

        rec = dispatch.dispatch(signal, context)

        state.add_artifact("_authority_residue_recommendation", {
            "signal": signal,
            "lens_id": rec.lens_id,
            "oddity_preserved": rec.oddity_preserved,
            "first_response": rec.first_response,
            "escalate_to": rec.escalate_to,
            "notes": rec.notes,
            "invoked_at": __import__("datetime").datetime.now().isoformat(),
        })
    
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
