"""Concurrent helpers for independent pipeline execution."""

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from concurrent.futures import ThreadPoolExecutor

from runtime.execution.dispatcher import RuntimeDispatcher
from runtime.state.models import ExecutionState, FamilyType


@dataclass
class PipelineRequest:
    """One independent pipeline execution request."""

    family: FamilyType
    pipeline_id: str
    state: ExecutionState
    context: Dict[str, Any]


class ConcurrentRuntimeExecutor:
    """Run independent pipelines concurrently against one dispatcher."""

    def __init__(
        self,
        output_path: Path,
        dispatcher: Optional[RuntimeDispatcher] = None,
    ):
        self.output_path = Path(output_path)
        self.dispatcher = dispatcher or RuntimeDispatcher(self.output_path)

    def execute(
        self,
        requests: Iterable[PipelineRequest],
        max_workers: int = 4,
    ) -> List[ExecutionState]:
        """Execute independent requests concurrently and return their final states."""
        request_list = list(requests)
        if not request_list:
            return []

        worker_count = max(1, min(max_workers, len(request_list)))
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = [
                executor.submit(
                    self.dispatcher.execute_pipeline,
                    request.family,
                    request.pipeline_id,
                    deepcopy(request.state),
                    deepcopy(request.context),
                )
                for request in request_list
            ]
            return [future.result() for future in futures]
