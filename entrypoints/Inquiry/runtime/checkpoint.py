"""
Checkpoint system for state persistence.

See: docs/execution_order_table.md - Checkpoint Order
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from runtime.state.models import ExecutionState, RouteDecision


class CheckpointManager:
    """
    Manages state checkpoints during pipeline execution.
    
    Checkpoints are created:
    - After each pipeline completes
    - Before cross-family transitions
    - On explicit request
    """
    
    def __init__(self, checkpoint_dir: Path):
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def create_checkpoint(
        self,
        state: ExecutionState,
        route_history: List[RouteDecision],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a state checkpoint.
        
        Args:
            state: Current execution state
            route_history: Route decision history
            metadata: Optional checkpoint metadata
            
        Returns:
            Checkpoint ID (timestamp-based)
        """
        checkpoint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        checkpoint_data = {
            "checkpoint_id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "state": self._serialize_state(state),
            "route_history": [r.to_dict() for r in route_history],
            "metadata": metadata or {},
        }
        
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        checkpoint_path.write_text(json.dumps(checkpoint_data, indent=2))
        
        return checkpoint_id
    
    def load_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """
        Load a checkpoint by ID.
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            Checkpoint data dictionary
        """
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
        
        return json.loads(checkpoint_path.read_text())
    
    def list_checkpoints(self) -> List[Dict[str, str]]:
        """List all checkpoints with metadata."""
        checkpoints = []
        
        for path in sorted(self.checkpoint_dir.glob("*.json")):
            data = json.loads(path.read_text())
            checkpoints.append({
                "id": data["checkpoint_id"],
                "timestamp": data["timestamp"],
                "pipeline": data["state"].get("current_pipeline", "unknown"),
                "family": data["state"].get("current_family", "unknown"),
            })
        
        return checkpoints
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            return True
        return False
    
    def _serialize_state(self, state: ExecutionState) -> Dict[str, Any]:
        """Serialize execution state to JSON-serializable dict."""
        return {
            "current_family": state.current_family.value,
            "current_pipeline": state.current_pipeline,
            "current_phase": state.current_phase,
            "phase_index": state.phase_index,
            "artifacts": list(state.artifacts.keys()),  # Just names, not full data
            "trust_assessment": (
                {
                    "trust_level": state.trust_assessment.trust_level,
                    "entropy_level": state.trust_assessment.entropy_level,
                    "coherence_restored": state.trust_assessment.coherence_restored,
                }
                if state.trust_assessment
                else None
            ),
            "errors": state.errors,
            "unresolveds": state.unresolveds,
        }
    
    def get_latest_checkpoint(self) -> Optional[Dict[str, Any]]:
        """Get the most recent checkpoint."""
        checkpoints = self.list_checkpoints()
        
        if not checkpoints:
            return None
        
        latest = checkpoints[-1]
        return self.load_checkpoint(latest["id"])
