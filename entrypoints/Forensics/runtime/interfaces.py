"""
Interfaces for external integrations.

See: docs/implementation/hook_and_interface_contract.md
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from runtime.state.models import ExecutionState


class ExternalAPI(ABC):
    """
    Interface for external API integrations.
    
    Implement this to connect the runtime to external services.
    """
    
    @abstractmethod
    def notify_pipeline_start(self, pipeline_id: str, context: Dict) -> None:
        """Notify external service of pipeline start."""
        pass
    
    @abstractmethod
    def notify_pipeline_complete(
        self,
        pipeline_id: str,
        artifacts: Dict[str, Any],
    ) -> None:
        """Notify external service of pipeline completion."""
        pass
    
    @abstractmethod
    def notify_error(self, error: str, state: ExecutionState) -> None:
        """Notify external service of error."""
        pass
    
    @abstractmethod
    def fetch_external_data(self, source: str) -> Any:
        """Fetch data from external source."""
        pass


class StorageBackend(ABC):
    """
    Interface for custom storage backends.
    
    Implement this for custom persistence (S3, database, etc.).
    """
    
    @abstractmethod
    def save_checkpoint(self, state: ExecutionState) -> str:
        """
        Save state checkpoint.
        
        Returns:
            Checkpoint ID
        """
        pass
    
    @abstractmethod
    def load_checkpoint(self, checkpoint_id: str) -> ExecutionState:
        """Load state from checkpoint."""
        pass
    
    @abstractmethod
    def save_artifact(
        self,
        name: str,
        data: Any,
        provenance: Dict[str, Any],
    ) -> None:
        """Save artifact with provenance."""
        pass
    
    @abstractmethod
    def list_artifacts(self, pipeline_id: str) -> List[str]:
        """List artifact names for a pipeline."""
        pass


class Logger(ABC):
    """
    Interface for external logging.
    
    Implement this for custom logging (ELK, Datadog, etc.).
    """
    
    @abstractmethod
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log structured event."""
        pass
    
    @abstractmethod
    def log_metric(self, name: str, value: float, tags: Dict[str, str]) -> None:
        """Log numeric metric."""
        pass
    
    @abstractmethod
    def log_trace(
        self,
        trace_id: str,
        span_id: str,
        data: Dict[str, Any],
    ) -> None:
        """Log distributed trace span."""
        pass


# Default in-memory implementations

class InMemoryStorage(StorageBackend):
    """In-memory storage backend for testing."""
    
    def __init__(self):
        self._checkpoints: Dict[str, ExecutionState] = {}
        self._artifacts: Dict[str, Dict[str, Any]] = {}
    
    def save_checkpoint(self, state: ExecutionState) -> str:
        import uuid
        checkpoint_id = str(uuid.uuid4())
        self._checkpoints[checkpoint_id] = state
        return checkpoint_id
    
    def load_checkpoint(self, checkpoint_id: str) -> ExecutionState:
        if checkpoint_id not in self._checkpoints:
            raise KeyError(f"Checkpoint not found: {checkpoint_id}")
        return self._checkpoints[checkpoint_id]
    
    def save_artifact(
        self,
        name: str,
        data: Any,
        provenance: Dict[str, Any],
    ) -> None:
        key = f"{provenance.get('pipeline', 'unknown')}/{name}"
        self._artifacts[key] = {
            "data": data,
            "provenance": provenance,
        }
    
    def list_artifacts(self, pipeline_id: str) -> List[str]:
        prefix = f"{pipeline_id}/"
        return [
            k[len(prefix):]
            for k in self._artifacts.keys()
            if k.startswith(prefix)
        ]


class ConsoleLogger(Logger):
    """Console logger for development."""
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        print(f"[EVENT {event_type}] {data}")
    
    def log_metric(self, name: str, value: float, tags: Dict[str, str]) -> None:
        tag_str = ", ".join(f"{k}={v}" for k, v in tags.items())
        print(f"[METRIC {name}={value}] {tag_str}")
    
    def log_trace(
        self,
        trace_id: str,
        span_id: str,
        data: Dict[str, Any],
    ) -> None:
        print(f"[TRACE {trace_id}/{span_id}] {data}")
