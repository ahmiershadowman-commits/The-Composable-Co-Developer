from pathlib import Path

from runtime.execution.concurrent import ConcurrentRuntimeExecutor, PipelineRequest
from runtime.state.models import ExecutionState, FamilyType


class _StubDispatcher:
    def __init__(self):
        self.calls = []

    def execute_pipeline(self, family, pipeline_id, state, context):
        self.calls.append((family, pipeline_id, context))
        state.current_pipeline = pipeline_id
        state.add_artifact("result", {"family": family.value, "context": context})
        return state


def test_concurrent_runtime_executor_runs_independent_requests(tmp_path):
    dispatcher = _StubDispatcher()
    executor = ConcurrentRuntimeExecutor(Path(tmp_path), dispatcher=dispatcher)

    results = executor.execute(
        [
            PipelineRequest(
                family=FamilyType.FORENSICS,
                pipeline_id="project_mapping",
                state=ExecutionState(current_family=FamilyType.FORENSICS),
                context={"scope": "repo"},
            ),
            PipelineRequest(
                family=FamilyType.CONDUIT,
                pipeline_id="documentation",
                state=ExecutionState(current_family=FamilyType.CONDUIT),
                context={"audience": "engineering"},
            ),
        ],
        max_workers=2,
    )

    assert len(results) == 2
    assert {result.current_pipeline for result in results} == {
        "project_mapping",
        "documentation",
    }
    assert len(dispatcher.calls) == 2
