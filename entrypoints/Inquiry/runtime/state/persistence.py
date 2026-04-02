"""
Persistence layer for execution state.

Provides checkpointing and state recovery for long-running
pipeline executions.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

from runtime.state.models import (
    ExecutionState,
    TrustAssessment,
    FamilyType,
    RouteDecision,
    RouteAction,
    InterventionBand,
)


class StatePersistence:
    """
    Persists and recovers execution state.
    
    Enables checkpointing for long-running executions
    and recovery from interruptions.
    """
    
    def __init__(self, checkpoint_dir: Path):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(
        self,
        state: ExecutionState,
        execution_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Path:
        """
        Save execution state checkpoint.
        
        Args:
            state: Current execution state
            execution_id: Unique execution identifier
            metadata: Optional metadata about the checkpoint
        
        Returns:
            Path to checkpoint file
        """
        checkpoint_data = {
            "execution_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "state": self._serialize_state(state),
            "metadata": metadata or {},
        }
        
        checkpoint_path = self.checkpoint_dir / f"{execution_id}.yaml"
        
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            yaml.dump(checkpoint_data, f, default_flow_style=False, sort_keys=False)
        
        return checkpoint_path
    
    def load_checkpoint(
        self,
        execution_id: str,
    ) -> Optional[ExecutionState]:
        """
        Load execution state from checkpoint.
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            Restored ExecutionState or None if not found
        """
        checkpoint_path = self.checkpoint_dir / f"{execution_id}.yaml"
        
        if not checkpoint_path.exists():
            return None
        
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            checkpoint_data = yaml.safe_load(f)
        
        return self._deserialize_state(checkpoint_data["state"])
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints."""
        checkpoints = []
        
        for checkpoint_file in self.checkpoint_dir.glob("*.yaml"):
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                checkpoints.append({
                    "execution_id": data.get("execution_id"),
                    "timestamp": data.get("timestamp"),
                    "path": str(checkpoint_file),
                })
        
        return sorted(checkpoints, key=lambda x: x["timestamp"], reverse=True)
    
    def delete_checkpoint(self, execution_id: str) -> bool:
        """Delete a checkpoint."""
        checkpoint_path = self.checkpoint_dir / f"{execution_id}.yaml"
        
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            return True
        return False
    
    def _serialize_state(self, state: ExecutionState) -> Dict[str, Any]:
        """Serialize ExecutionState to dict."""
        return {
            "current_family": state.current_family.value,
            "current_pipeline": state.current_pipeline,
            "current_phase": state.current_phase,
            "phase_index": state.phase_index,
            "artifacts": self._serialize_artifacts(state.artifacts),
            "route_history": [self._serialize_route_decision(d) for d in state.route_history],
            "trust_assessment": self._serialize_trust_assessment(state.trust_assessment),
            "residue_preserved": state.residue_preserved,
            "unresolveds": state.unresolveds,
            "errors": state.errors,
            "started_at": state.started_at.isoformat(),
        }
    
    def _deserialize_state(self, data: Dict[str, Any]) -> ExecutionState:
        """Deserialize dict to ExecutionState."""
        # Convert family string to enum
        family = FamilyType(data["current_family"])
        
        # Parse datetime
        started_at = datetime.fromisoformat(data["started_at"])
        
        # Deserialize route history
        route_history = [
            self._deserialize_route_decision(d) 
            for d in data.get("route_history", [])
        ]
        
        # Deserialize trust assessment
        trust_assessment = None
        if data.get("trust_assessment"):
            trust_assessment = self._deserialize_trust_assessment(data["trust_assessment"])
        
        return ExecutionState(
            current_family=family,
            current_pipeline=data.get("current_pipeline"),
            current_phase=data.get("current_phase"),
            phase_index=data.get("phase_index", 0),
            artifacts=data.get("artifacts", {}),
            route_history=route_history,
            trust_assessment=trust_assessment,
            residue_preserved=data.get("residue_preserved", {}),
            unresolveds=data.get("unresolveds", []),
            errors=data.get("errors", []),
            started_at=started_at,
        )
    
    def _serialize_artifacts(self, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize artifacts, handling non-serializable types."""
        serialized = {}
        for name, data in artifacts.items():
            if isinstance(data, (dict, list, str, int, float, bool, type(None))):
                serialized[name] = data
            else:
                serialized[name] = str(data)
        return serialized
    
    def _serialize_route_decision(self, decision: RouteDecision) -> Dict[str, Any]:
        """Serialize RouteDecision to dict."""
        return decision.to_dict()
    
    def _deserialize_route_decision(self, data: Dict[str, Any]) -> RouteDecision:
        """Deserialize dict to RouteDecision."""
        return RouteDecision(
            action=RouteAction(data["action"]),
            target=data["target"],
            intervention_band=InterventionBand(data["intervention_band"]),
            reason=data["reason"],
            phase_index=data.get("phase_index"),
            pipeline_id=data.get("pipeline_id"),
            family=FamilyType(data["family"]) if data.get("family") else None,
            authority_data=data.get("authority_data"),
            residue_to_preserve=data.get("residue_to_preserve", {}),
        )
    
    def _serialize_trust_assessment(
        self,
        trust: Optional[TrustAssessment],
    ) -> Optional[Dict[str, Any]]:
        """Serialize TrustAssessment to dict."""
        if not trust:
            return None
        
        return {
            "trust_level": trust.trust_level,
            "canonical_sources_identified": trust.canonical_sources_identified,
            "discrepancy_count": trust.discrepancy_count,
            "entropy_level": trust.entropy_level,
            "coherence_restored": trust.coherence_restored,
            "requires_forensics": trust.requires_forensics,
            "requires_defragmentation": trust.requires_defragmentation,
            "notes": trust.notes,
            "assessed_at": trust.assessed_at.isoformat(),
        }
    
    def _deserialize_trust_assessment(
        self,
        data: Dict[str, Any],
    ) -> TrustAssessment:
        """Deserialize dict to TrustAssessment."""
        return TrustAssessment(
            trust_level=data["trust_level"],
            canonical_sources_identified=data.get("canonical_sources_identified", False),
            discrepancy_count=data.get("discrepancy_count", 0),
            entropy_level=data.get("entropy_level", "low"),
            coherence_restored=data.get("coherence_restored", False),
            requires_forensics=data.get("requires_forensics", False),
            requires_defragmentation=data.get("requires_defragmentation", False),
            notes=data.get("notes", []),
            assessed_at=datetime.fromisoformat(data["assessed_at"]),
        )


class ExecutionLog:
    """
    Execution log for audit trail.
    
    Records all significant events during execution.
    """
    
    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / "execution.log"
    
    def log_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        execution_id: Optional[str] = None,
    ) -> None:
        """Log an execution event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "execution_id": execution_id,
            "details": details,
        }
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + "\n")
    
    def log_pipeline_start(
        self,
        family: str,
        pipeline_id: str,
        execution_id: str,
    ) -> None:
        """Log pipeline start."""
        self.log_event("pipeline_start", {
            "family": family,
            "pipeline_id": pipeline_id,
        }, execution_id)
    
    def log_pipeline_complete(
        self,
        family: str,
        pipeline_id: str,
        execution_id: str,
        artifacts_produced: List[str],
    ) -> None:
        """Log pipeline completion."""
        self.log_event("pipeline_complete", {
            "family": family,
            "pipeline_id": pipeline_id,
            "artifacts_produced": artifacts_produced,
        }, execution_id)
    
    def log_error(
        self,
        error: str,
        execution_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an error."""
        self.log_event("error", {
            "error": error,
            "context": context or {},
        }, execution_id)
    
    def log_transition(
        self,
        from_state: Dict[str, Any],
        to_state: Dict[str, Any],
        execution_id: str,
    ) -> None:
        """Log a state transition."""
        self.log_event("transition", {
            "from": from_state,
            "to": to_state,
        }, execution_id)
    
    def get_execution_log(self, execution_id: str) -> List[Dict[str, Any]]:
        """Get all log entries for an execution."""
        entries = []
        
        if not self.log_path.exists():
            return entries
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("execution_id") == execution_id:
                    entries.append(entry)
        
        return entries
