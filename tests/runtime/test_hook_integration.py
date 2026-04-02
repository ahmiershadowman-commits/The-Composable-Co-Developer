from pathlib import Path

from runtime.execution.dispatcher import RuntimeDispatcher
from runtime.state.models import ExecutionState, FamilyType


def test_pre_pipeline_hook_blocks_missing_forge_problem():
    dispatcher = RuntimeDispatcher(Path("runtime_output"))
    state = ExecutionState(current_family=FamilyType.FORGE)

    result = dispatcher.execute_pipeline(FamilyType.FORGE, "development", state, {})

    assert result.errors
    assert "Forge pipeline requires 'problem' in context" in result.errors[0]


def test_dispatcher_loads_managed_mcp_registry():
    dispatcher = RuntimeDispatcher(Path("runtime_output"))
    assert dispatcher.managed_mcp is not None
    assert dispatcher.managed_mcp.get("github-managed") is not None
