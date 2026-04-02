"""
Hook context and result types.

See: docs/implementation/hook_and_interface_contract.md
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from runtime.state.models import ExecutionState


@dataclass
class HookContext:
    """
    Standard context object passed to all hooks.
    
    Attributes:
        session_id: Unique session identifier
        pipeline_id: Current pipeline (e.g., "Forensics/project_mapping")
        phase_id: Current phase or None
        state: Current execution state
        context: Pipeline context data
        timestamp: ISO format timestamp
    """
    session_id: str
    pipeline_id: str
    phase_id: Optional[str]
    state: ExecutionState
    context: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "pipeline_id": self.pipeline_id,
            "phase_id": self.phase_id,
            "state": {
                "current_family": self.state.current_family.value,
                "current_pipeline": self.state.current_pipeline,
                "current_phase": self.state.current_phase,
                "artifact_count": len(self.state.artifacts),
                "error_count": len(self.state.errors),
            },
            "context": self.context,
            "timestamp": self.timestamp,
        }


@dataclass
class HookResult:
    """
    Standard result object returned by hooks.
    
    Attributes:
        continue_execution: False to halt execution
        modifications: State/context modifications to apply
        error_message: Error message if hook failed
    """
    continue_execution: bool = True
    modifications: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "continue_execution": self.continue_execution,
            "modifications": self.modifications,
            "error_message": self.error_message,
        }
    
    @classmethod
    def success(cls, modifications: Optional[Dict[str, Any]] = None) -> "HookResult":
        """Create a success result."""
        return cls(
            continue_execution=True,
            modifications=modifications or {},
        )
    
    @classmethod
    def halt(cls, error_message: str) -> "HookResult":
        """Create a halt result."""
        return cls(
            continue_execution=False,
            error_message=error_message,
        )
