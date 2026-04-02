"""Selector schema for the marketplace runtime.

Selectors are persistent low-cost controllers. They are not full agents.
They should remain small, legible, and threshold-driven.

A selector owns:
- motif bias
- rubric/checklist references
- trigger interpretation
- smallest-sufficient intervention preference
- escalation boundaries

A selector does not own:
- heavyweight evaluation itself
- family-wide policy
- deep forensic truth establishment
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Literal, Optional


class Family(str, Enum):
    FORENSICS = "Forensics"
    FORGE = "Forge"
    INQUIRY = "Inquiry"
    CONDUIT = "Conduit"


class InterventionLevel(int, Enum):
    CONTINUE = 0
    MOTIF_NUDGE = 1
    PRIMITIVE = 2
    SELF_CHECK = 3
    LOCAL_EVALUATOR = 4
    WITHIN_PIPELINE_PIVOT = 5
    SIBLING_PIPELINE_SHIFT = 6
    HEAVY_EVALUATOR_OR_SYNTHESIS = 7
    CROSS_FAMILY_REROUTE = 8
    FORENSICS_RESET = 9


class TriggerClass(str, Enum):
    PHASE_FIT = "phase_fit"
    METHOD_FIT = "method_fit"
    ARTIFACT_DRIFT = "artifact_drift"
    METADATA_DRIFT = "metadata_drift"
    CONTRADICTION = "contradiction"
    CONFIDENCE_SUPPORT_MISMATCH = "confidence_support_mismatch"
    REPEATED_FAILURE = "repeated_failure"
    BRANCH_SPRAWL = "branch_sprawl"
    TRUST_COLLAPSE = "trust_collapse"
    CLEANUP_NEEDED = "cleanup_needed"
    SYNTHESIS_NEEDED = "synthesis_needed"
    REROUTE_AMBIGUITY = "reroute_ambiguity"


class PrimitiveName(str, Enum):
    CENTER = "center"
    OPEN = "open"
    TRIM = "trim"
    SHIFT = "shift"
    HOLD = "hold"
    REREAD = "reread"
    PRESS = "press"
    WEAVE = "weave"
    LOCATE = "locate"
    RELEASE = "release"


ActionKind = Literal[
    "continue",
    "motif_nudge",
    "primitive",
    "self_check",
    "local_evaluator",
    "pivot",
    "sibling_shift",
    "heavy_call",
    "reroute",
    "forensics_reset",
]


@dataclass(slots=True)
class MotifBias:
    primary: Optional[str] = None
    secondary: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass(slots=True)
class ActionDirective:
    kind: ActionKind
    target: Optional[str] = None
    reason: Optional[str] = None
    intervention_level: InterventionLevel = InterventionLevel.CONTINUE
    preserve_residue: bool = True


@dataclass(slots=True)
class TriggerPolicy:
    name: str
    trigger_class: TriggerClass
    preferred_action: ActionDirective
    fallback_action: Optional[ActionDirective] = None
    notes: str = ""


@dataclass(slots=True)
class SelectorConfig:
    selector_id: str
    family: Family
    pipeline_scope: List[str]
    motif_bias: MotifBias = field(default_factory=MotifBias)
    rubric_ref: Optional[str] = None
    checklist_ref: Optional[str] = None
    trigger_glossary_ref: Optional[str] = None
    smallest_sufficient_default: InterventionLevel = InterventionLevel.PRIMITIVE
    trigger_policies: List[TriggerPolicy] = field(default_factory=list)
    exit_checks: List[str] = field(default_factory=list)
    escalation_boundary: InterventionLevel = InterventionLevel.LOCAL_EVALUATOR
    notes: str = ""


@dataclass(slots=True)
class SelectorDecision:
    selector_id: str
    observed_triggers: List[TriggerClass]
    chosen_action: ActionDirective
    rationale: str
    residue_to_preserve: List[str] = field(default_factory=list)
    followup_checks: List[str] = field(default_factory=list)


__all__ = [
    "Family",
    "InterventionLevel",
    "TriggerClass",
    "PrimitiveName",
    "MotifBias",
    "ActionDirective",
    "TriggerPolicy",
    "SelectorConfig",
    "SelectorDecision",
]
