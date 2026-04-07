"""
Trigger ownership enforcement hook.

Implements the trigger ownership model from trigger_patterns.md:

  Trace  → routine micro-checks, smallest-sufficient intervention choice
  Residue → suspicious-surface interpretation, lens-based first responses
  Lever  → evaluator invocation, explicit adjudication, escalation

This hook fires on PreTransition events and blocks shortcuts that violate
the ownership hierarchy before they reach the TransitionEngine.

See: docs/implementation/trigger_patterns.md
"""

from hooks.context import HookContext, HookResult

# ---------------------------------------------------------------------------
# Authority ownership rules
# ---------------------------------------------------------------------------

# Lever evaluator IDs that require Trace to have been consulted first.
_LEVER_EVALUATOR_IDS = {
    "contradiction_evaluator",
    "discriminator_evaluator",
    "support_evaluator",
    "frame_evaluator",
    "trust_evaluator",
    "artifact_shape_evaluator",
}

# Residue signals that should NEVER skip to Lever without Trace first.
_RESIDUE_ONLY_SIGNALS = {
    "misfit_detected",
    "absence_detected",
    "tension_detected",
    "warp_detected",
    "offset_detected",
}

# Triggers that *require* cross-family reroute (Trace can't handle locally).
_TRUST_COLLAPSE_INDICATORS = {
    "trust_collapse",
    "trust_collapsed",
    "canonical_conflict_critical",
}


def trigger_ownership_hook(context: HookContext) -> HookResult:
    """
    Enforce trigger ownership before a transition executes.

    Checks (in order):
    1. Lever must not be called before Trace has attempted smallest-sufficient handling.
    2. Residue must not substitute for explicit evaluator adjudication.
    3. Cross-family reroute must not be triggered when a legal local intervention remains.
    4. Residue-level signals must not bypass Residue and go straight to Lever.
    """
    ctx = context.context
    state = context.state

    # -----------------------------------------------------------------------
    # Extract pending transition info from hook context
    # The TransitionEngine caller is expected to populate these keys:
    #   pending_action   : str  (e.g. "authority_call", "cross_family_reroute")
    #   pending_target   : str  (e.g. "authority:Lever", "family:Forensics")
    #   pending_trigger  : str  (the trigger ID that caused this transition)
    # -----------------------------------------------------------------------
    action = ctx.get("pending_action", "")
    target = ctx.get("pending_target", "")
    trigger = ctx.get("pending_trigger", "")
    authority_data = ctx.get("pending_authority_data", {})

    if not action:
        # No pending transition info — hook is a no-op
        return HookResult.success()

    # -----------------------------------------------------------------------
    # Rule 1: Lever must not be called before Trace has attempted handling.
    # -----------------------------------------------------------------------
    if action == "authority_call" and target == "authority:Lever":
        trace_consulted = (
            ctx.get("trace_consulted")
            or "_authority_trace_evaluation" in state.artifacts
        )
        if not trace_consulted:
            evaluator_id = authority_data.get("evaluator_id", "<unknown>")
            return HookResult.halt(
                f"Trigger ownership violation: Lever evaluator '{evaluator_id}' called before "
                "Trace attempted smallest-sufficient handling. "
                "Invoke authority:Trace first (or set 'trace_consulted': true in context if "
                "Trace has already evaluated this state)."
            )

    # -----------------------------------------------------------------------
    # Rule 2: Residue must not substitute for evaluator adjudication.
    # -----------------------------------------------------------------------
    if action == "authority_call" and target == "authority:Residue":
        residue_signal = authority_data.get("signal", trigger)
        # If the signal is not a Residue-domain signal, block it.
        if residue_signal and residue_signal not in _RESIDUE_ONLY_SIGNALS:
            # Check if there is an unresolved adjudication need in state
            needs_adjudication = any(
                k in state.artifacts for k in (
                    "contradictions_detected",
                    "support_gap",
                    "frame_error_risk",
                    "discriminator_required",
                )
            )
            if needs_adjudication:
                return HookResult.halt(
                    f"Trigger ownership violation: Residue called with signal '{residue_signal}' "
                    "while adjudication-requiring artifacts are present. "
                    "Use authority:Lever with the appropriate evaluator for explicit adjudication."
                )

    # -----------------------------------------------------------------------
    # Rule 3: Cross-family reroute must not shortcut when local intervention
    #         is available.
    # -----------------------------------------------------------------------
    if action == "cross_family_reroute":
        # Allow if trust collapse is confirmed
        trust_collapsed = (
            any(k in state.artifacts for k in _TRUST_COLLAPSE_INDICATORS)
            or ctx.get("trust_collapsed")
            or (state.trust_assessment is not None and state.trust_assessment.requires_forensics)
        )
        if not trust_collapsed:
            # Check whether a local pivot is still available
            local_pivot_available = ctx.get("local_pivot_available")
            if local_pivot_available:
                return HookResult.halt(
                    "Trigger ownership violation: cross-family reroute triggered while a legal "
                    "local intervention ('local_pivot_available' is set) remains. "
                    "Apply the smallest-sufficient local intervention first."
                )

    # -----------------------------------------------------------------------
    # Rule 4: Residue-domain signals must not bypass Residue → Lever chain.
    # -----------------------------------------------------------------------
    if (
        action == "authority_call"
        and target == "authority:Lever"
        and trigger in _RESIDUE_ONLY_SIGNALS
    ):
        residue_consulted = (
            ctx.get("residue_consulted")
            or "_authority_residue_recommendation" in state.artifacts
        )
        if not residue_consulted:
            return HookResult.halt(
                f"Trigger ownership violation: Lever called for Residue-domain signal '{trigger}' "
                "without first consulting Residue. "
                "Dispatch to authority:Residue first to apply lens-based first response."
            )

    return HookResult.success()
