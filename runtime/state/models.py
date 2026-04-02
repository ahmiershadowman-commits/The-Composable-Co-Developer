"""
Runtime state models for the composable co-developer.

Defines core state objects used throughout execution:
- RuntimeContext: Current execution context
- ExecutionState: Mutable state during pipeline execution
- RouteDecision: Structured routing decision from Trace
- ArtifactRecord: Record of emitted artifacts
- TrustAssessment: Trust evaluation of current state surface
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class FamilyType(str, Enum):
    """Valid family types."""
    FORENSICS = "Forensics"
    FORGE = "Forge"
    INQUIRY = "Inquiry"
    CONDUIT = "Conduit"


class AuthorityType(str, Enum):
    """Shared authority types."""
    TRACE = "Trace"
    LEVER = "Lever"
    RESIDUE = "Residue"


class InterventionBand(int, Enum):
    """Intervention severity bands."""
    MOTIF = 1
    PRIMITIVE = 2
    SELECTOR_SELF_CHECK = 3
    LOCAL_EVALUATOR = 4
    PHASE_PIVOT = 5
    SIBLING_PIPELINE_SHIFT = 6
    HEAVY_SKILL = 7
    CROSS_FAMILY_REROUTE = 8
    FORENSICS_RESET = 9


class RouteAction(str, Enum):
    """Types of routing actions."""
    CONTINUE = "continue"
    PHASE_PIVOT = "phase_pivot"
    SIBLING_SHIFT = "sibling_shift"
    CROSS_FAMILY_REROUTE = "cross_family_reroute"
    AUTHORITY_CALL = "authority_call"
    FORENSICS_RESET = "forensics_reset"


@dataclass
class RuntimeContext:
    """
    Immutable context for runtime execution.
    
    Contains configuration and references that don't change
    during execution.
    """
    repo_root: Path
    bundle_path: Path
    output_path: Path
    family: FamilyType
    pipeline_id: Optional[str] = None
    phase_id: Optional[str] = None
    
    def __post_init__(self):
        if isinstance(self.repo_root, str):
            self.repo_root = Path(self.repo_root)
        if isinstance(self.bundle_path, str):
            self.bundle_path = Path(self.bundle_path)
        if isinstance(self.output_path, str):
            self.output_path = Path(self.output_path)


@dataclass
class ExecutionState:
    """
    Mutable state during pipeline execution.
    
    Tracks progress, artifacts, and routing history.
    """
    current_family: FamilyType
    current_pipeline: Optional[str] = None
    current_phase: Optional[str] = None
    phase_index: int = 0
    artifacts: Dict[str, Any] = field(default_factory=dict)
    route_history: List["RouteDecision"] = field(default_factory=list)
    trust_assessment: Optional["TrustAssessment"] = None
    residue_preserved: Dict[str, Any] = field(default_factory=dict)
    unresolveds: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    
    def add_artifact(self, name: str, data: Any) -> None:
        """Record an artifact."""
        self.artifacts[name] = data
    
    def add_route_decision(self, decision: "RouteDecision") -> None:
        """Record a routing decision."""
        self.route_history.append(decision)
    
    def add_error(self, error: str) -> None:
        """Record an error."""
        self.errors.append(error)

    def add_metadata(self, key: str, value: Any) -> None:
        """Record non-artifact execution metadata."""
        self.metadata[key] = value
    
    def can_proceed(self) -> bool:
        """Check if execution can continue."""
        return len(self.errors) == 0


@dataclass
class RouteDecision:
    """
    Structured routing decision from Trace.
    
    Represents the output of Trace's smallest-sufficient
    intervention selection.
    """
    action: RouteAction
    target: str
    intervention_band: InterventionBand
    reason: str
    phase_index: Optional[int] = None
    pipeline_id: Optional[str] = None
    family: Optional[FamilyType] = None
    authority_data: Optional[Dict[str, Any]] = None
    residue_to_preserve: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "action": self.action.value,
            "target": self.target,
            "intervention_band": self.intervention_band.value,
            "reason": self.reason,
            "phase_index": self.phase_index,
            "pipeline_id": self.pipeline_id,
            "family": self.family.value if self.family else None,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ArtifactRecord:
    """
    Record of an emitted artifact.
    
    Tracks artifact metadata for provenance.
    """
    name: str
    path: Path
    artifact_type: str
    pipeline: str
    family: FamilyType
    created_at: datetime = field(default_factory=datetime.now)
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.path, str):
            self.path = Path(self.path)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "path": str(self.path),
            "artifact_type": self.artifact_type,
            "pipeline": self.pipeline,
            "family": self.family.value,
            "created_at": self.created_at.isoformat(),
            "checksum": self.checksum,
            "metadata": self.metadata,
        }


@dataclass
class TrustAssessment:
    """
    Assessment of trust in the current state surface.
    
    Used by Forensics and Trace to determine if execution
    can safely proceed.
    """
    trust_level: str  # "high", "medium", "low", "collapsed"
    canonical_sources_identified: bool = False
    discrepancy_count: int = 0
    entropy_level: str = "low"  # "low", "medium", "high"
    coherence_restored: bool = False
    requires_forensics: bool = False
    requires_defragmentation: bool = False
    notes: List[str] = field(default_factory=list)
    assessed_at: datetime = field(default_factory=datetime.now)
    
    def is_trustworthy(self) -> bool:
        """Check if surface is trustworthy enough to proceed."""
        return self.trust_level in ("high", "medium") and not self.requires_forensics
    
    def should_reroute_to_forensics(self) -> bool:
        """Check if reroute to Forensics is needed."""
        return self.requires_forensics or self.trust_level == "collapsed"
    
    def should_reroute_to_defragmentation(self) -> bool:
        """Check if reroute to defragmentation is needed."""
        return self.requires_defragmentation or self.entropy_level == "high"
