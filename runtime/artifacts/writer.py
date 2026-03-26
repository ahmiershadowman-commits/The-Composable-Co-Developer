"""
Artifact writer for runtime outputs.

Writes artifacts, route history, provenance records,
and route recommendations to disk.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

from runtime.state.models import (
    ExecutionState,
    ArtifactRecord,
    FamilyType,
    RouteDecision,
)


class ArtifactWriter:
    """
    Writes artifacts and provenance to disk.
    
    Handles structured output of pipeline artifacts,
    route history, and provenance records.
    """
    
    def __init__(self, output_path: Path):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.artifacts_written: List[ArtifactRecord] = []
    
    def write_artifact(
        self,
        name: str,
        data: Any,
        pipeline: str,
        family: FamilyType,
        artifact_type: str = "data",
    ) -> Optional[ArtifactRecord]:
        """
        Write an artifact to disk.
        
        Returns ArtifactRecord or None on failure.
        """
        try:
            # Create family/pipeline directory
            artifact_dir = self.output_path / family.value / pipeline
            artifact_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine file extension and write
            if isinstance(data, (dict, list)):
                file_path = artifact_dir / f"{name}.yaml"
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            else:
                file_path = artifact_dir / f"{name}.txt"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            # Create record
            record = ArtifactRecord(
                name=name,
                path=file_path,
                artifact_type=artifact_type,
                pipeline=pipeline,
                family=family,
            )
            
            self.artifacts_written.append(record)
            return record
            
        except Exception as e:
            print(f"Error writing artifact {name}: {e}")
            return None
    
    def write_route_history(
        self,
        route_history: List[RouteDecision],
        pipeline: str,
        family: FamilyType,
    ) -> Optional[Path]:
        """Write route history to disk."""
        try:
            artifact_dir = self.output_path / family.value / pipeline
            artifact_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = artifact_dir / "route_history.yaml"
            
            history_data = [d.to_dict() for d in route_history]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(history_data, f, default_flow_style=False, sort_keys=False)
            
            return file_path
            
        except Exception as e:
            print(f"Error writing route history: {e}")
            return None
    
    def write_provenance(
        self,
        state: ExecutionState,
        pipeline: str,
        family: FamilyType,
    ) -> Optional[Path]:
        """Write provenance record for execution."""
        try:
            artifact_dir = self.output_path / family.value / pipeline
            artifact_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = artifact_dir / "provenance.yaml"
            
            provenance = {
                "pipeline": pipeline,
                "family": family.value,
                "started_at": state.started_at.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "route_decisions": len(state.route_history),
                "artifacts_produced": list(state.artifacts.keys()),
                "residue_preserved": state.residue_preserved,
                "unresolveds": state.unresolveds,
                "errors": state.errors,
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(provenance, f, default_flow_style=False, sort_keys=False)
            
            return file_path
            
        except Exception as e:
            print(f"Error writing provenance: {e}")
            return None
    
    def write_route_recommendation(
        self,
        recommendation: Dict[str, Any],
        pipeline: str,
        family: FamilyType,
    ) -> Optional[Path]:
        """Write route recommendation to disk."""
        try:
            artifact_dir = self.output_path / family.value / pipeline
            artifact_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = artifact_dir / "route_recommendation.yaml"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(recommendation, f, default_flow_style=False, sort_keys=False)
            
            return file_path
            
        except Exception as e:
            print(f"Error writing route recommendation: {e}")
            return None
    
    def write_state_snapshot(
        self,
        state: ExecutionState,
        pipeline: str,
        family: FamilyType,
    ) -> Optional[Path]:
        """Write current state snapshot."""
        try:
            artifact_dir = self.output_path / family.value / pipeline
            artifact_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = artifact_dir / "state_snapshot.yaml"
            
            snapshot = {
                "current_family": state.current_family.value,
                "current_pipeline": state.current_pipeline,
                "current_phase": state.current_phase,
                "phase_index": state.phase_index,
                "artifact_keys": list(state.artifacts.keys()),
                "route_history_count": len(state.route_history),
                "unresolveds": state.unresolveds,
                "errors": state.errors,
                "started_at": state.started_at.isoformat(),
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(snapshot, f, default_flow_style=False, sort_keys=False)
            
            return file_path
            
        except Exception as e:
            print(f"Error writing state snapshot: {e}")
            return None
    
    def get_artifact_summary(self) -> Dict[str, Any]:
        """Get summary of artifacts written."""
        return {
            "total_artifacts": len(self.artifacts_written),
            "artifacts": [
                {
                    "name": a.name,
                    "path": str(a.path),
                    "type": a.artifact_type,
                    "pipeline": a.pipeline,
                    "family": a.family.value,
                }
                for a in self.artifacts_written
            ],
        }
