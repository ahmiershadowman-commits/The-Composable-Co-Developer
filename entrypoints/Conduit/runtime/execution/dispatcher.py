"""
Runtime dispatcher for pipeline execution.

Integrates family executors with the runtime spine
to execute actual pipeline phases.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from runtime.state.models import ExecutionState, FamilyType
from hooks.context import HookContext
from hooks.post_pipeline import review_output_hook
from hooks.pre_pipeline import validate_entry_hook
from hooks.registry import HookEvent, HookRegistry
from runtime.mcp.registry import ManagedMCPRegistry
from runtime.mcp.session_host import ManagedMCPSessionHost
from runtime.execution.experimental import (
    ExperimentalApproval,
    ExperimentalApprovalError,
)
from runtime.visualization.report import RuntimeReportRenderer

# Import family executors
from entrypoints.Forensics.executors import ForensicsExecutor
from entrypoints.Forge.executors import ForgeExecutor
from entrypoints.Inquiry.executors import InquiryExecutor
from entrypoints.Conduit.executors import ConduitExecutor


# Experimental pipelines require explicit empirical approval.
EXPERIMENTAL_PIPELINES = {
    "Forensics": {"label_shift_correction", "introspection_audit"},
    "Inquiry": {"prompt_order_optimization", "human_hint_integration"},
}


class ExperimentalPipelineError(Exception):
    """Raised when an experimental pipeline is invoked."""
    pass


class RuntimeDispatcher:
    """
    Dispatches pipeline execution to appropriate family executor.

    Coordinates between runtime spine and family-specific
    execution logic.
    """

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.forensics = ForensicsExecutor(output_path)
        self.forge = ForgeExecutor(output_path)
        self.inquiry = InquiryExecutor(output_path)
        self.conduit = ConduitExecutor(output_path)
        self.hooks = self._build_hook_registry()
        self.managed_mcp = self._load_managed_mcp()
        self.mcp_host = self._build_mcp_host()
        self.report_renderer = RuntimeReportRenderer(output_path)

    def _build_hook_registry(self) -> HookRegistry:
        """Register the built-in python hooks used by the runtime spine."""
        registry = HookRegistry()
        registry.register(HookEvent.PRE_PIPELINE, validate_entry_hook, priority=10)
        registry.register(HookEvent.POST_PIPELINE, review_output_hook, priority=10)
        return registry

    def _load_managed_mcp(self) -> Optional[ManagedMCPRegistry]:
        """Load managed MCP config if the template exists at the repo root."""
        config_path = Path(__file__).resolve().parents[2] / "managed-mcp.json"
        if not config_path.exists():
            return None

        registry = ManagedMCPRegistry(config_path)
        registry.load()
        return registry

    def _build_mcp_host(self) -> Optional[ManagedMCPSessionHost]:
        """Build the managed MCP session host when a registry is available."""
        if self.managed_mcp is None:
            return None
        return ManagedMCPSessionHost(self.managed_mcp)

    def _make_hook_context(
        self,
        family: FamilyType,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> HookContext:
        """Create a hook context for the current pipeline execution."""
        return HookContext(
            session_id=f"{family.value}/{pipeline_id}",
            pipeline_id=f"{family.value}/{pipeline_id}",
            phase_id=state.current_phase,
            state=state,
            context=context,
        )

    def _guard_experimental(
        self,
        family_name: str,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> None:
        """
        Require approval for experimental pipelines.

        Call at the top of each _execute_* method.
        """
        blocked = EXPERIMENTAL_PIPELINES.get(family_name, set())
        if pipeline_id in blocked:
            try:
                approval = ExperimentalApproval.from_context(
                    context.get("experimental_approval")
                )
            except ExperimentalApprovalError as exc:
                raise ExperimentalPipelineError(str(exc)) from exc
            state.add_metadata(
                "experimental_approval",
                {"pipeline": f"{family_name}/{pipeline_id}", **approval.to_dict()},
            )

    def _connect_managed_mcp(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> bool:
        """Probe requested managed MCP endpoints before execution."""
        if self.mcp_host is None:
            return True

        requested = context.get("required_mcp", [])
        connect_all = bool(context.get("connect_all_mcp"))
        if not requested and not connect_all:
            return True

        sessions = self.mcp_host.connect_many(
            names=None if connect_all else requested,
            timeout_seconds=float(context.get("mcp_timeout_seconds", 2.0)),
        )
        session_payload = {
            name: session.to_dict() for name, session in sessions.items()
        }
        state.add_metadata("managed_mcp_sessions", session_payload)

        report_path = self.output_path / "_reports" / "managed_mcp_sessions.yaml"
        self.mcp_host.write_report(report_path)

        if bool(context.get("require_live_mcp")):
            failed = [name for name, session in sessions.items() if not session.connected]
            if failed:
                state.add_error(
                    "Managed MCP probe failed for: " + ", ".join(sorted(failed))
                )
                return False
        return True

    def _render_report(
        self,
        family: FamilyType,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> None:
        """Render an HTML execution report when requested."""
        if not bool(context.get("render_report")):
            return
        report_path = self.report_renderer.render(family.value, pipeline_id, state)
        state.add_metadata("report_path", str(report_path))

    def execute_pipeline(
        self,
        family: FamilyType,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute a pipeline by dispatching to family executor.
        
        Args:
            family: Target family
            pipeline_id: Pipeline identifier
            state: Current execution state
            context: Pipeline context and inputs
        
        Returns:
            Updated execution state
        """
        hook_context = self._make_hook_context(family, pipeline_id, state, context)
        pre_result = self.hooks.execute(HookEvent.PRE_PIPELINE, hook_context)
        if not pre_result.continue_execution:
            state.add_error(pre_result.error_message or "PrePipeline hook blocked execution")
            return state
        if not self._connect_managed_mcp(state, context):
            return state

        if family == FamilyType.FORENSICS:
            state = self._execute_forensics(pipeline_id, state, context)
        elif family == FamilyType.FORGE:
            state = self._execute_forge(pipeline_id, state, context)
        elif family == FamilyType.INQUIRY:
            state = self._execute_inquiry(pipeline_id, state, context)
        elif family == FamilyType.CONDUIT:
            state = self._execute_conduit(pipeline_id, state, context)
        else:
            state.add_error(f"Unknown family: {family}")
            return state

        post_result = self.hooks.execute(
            HookEvent.POST_PIPELINE,
            self._make_hook_context(family, pipeline_id, state, context),
        )
        if post_result.error_message:
            state.add_error(post_result.error_message)
        self._render_report(family, pipeline_id, state, context)
        return state
    
    def _execute_forensics(
        self,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute Forensics pipeline."""
        self._guard_experimental("Forensics", pipeline_id, state, context)
        if pipeline_id == "project_mapping":
            return self.forensics.execute_project_mapping(state, context)
        elif pipeline_id == "defragmentation":
            return self.forensics.execute_defragmentation(state, context)
        elif pipeline_id == "documentation_audit":
            return self.forensics.execute_documentation_audit(state, context)
        elif pipeline_id == "anomaly_disambiguation":
            return self.forensics.execute_anomaly_disambiguation(state, context)
        elif pipeline_id == "label_shift_correction":
            return self.forensics.execute_label_shift_correction(state, context)
        elif pipeline_id == "introspection_audit":
            return self.forensics.execute_introspection_audit(state, context)
        else:
            state.add_error(f"Unknown Forensics pipeline: {pipeline_id}")
            return state
    
    def _execute_forge(
        self,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute Forge pipeline."""
        self._guard_experimental("Forge", pipeline_id, state, context)
        if pipeline_id == "development":
            return self.forge.execute_development(state, context)
        elif pipeline_id == "coding":
            return self.forge.execute_coding(state, context)
        elif pipeline_id == "testing":
            return self.forge.execute_testing(state, context)
        elif pipeline_id == "refactor":
            return self.forge.execute_refactor(state, context)
        else:
            state.add_error(f"Unknown Forge pipeline: {pipeline_id}")
            return state
    
    def _execute_inquiry(
        self,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute Inquiry pipeline."""
        self._guard_experimental("Inquiry", pipeline_id, state, context)
        if pipeline_id == "research":
            return self.inquiry.execute_research(state, context)
        elif pipeline_id == "hypothesis_generation":
            return self.inquiry.execute_hypothesis_generation(state, context)
        elif pipeline_id == "data_analysis":
            return self.inquiry.execute_data_analysis(state, context)
        elif pipeline_id == "formalization":
            return self.inquiry.execute_formalization(state, context)
        elif pipeline_id == "mathematics":
            return self.inquiry.execute_mathematics(state, context)
        elif pipeline_id == "prompt_order_optimization":
            return self.inquiry.execute_prompt_order_optimization(state, context)
        elif pipeline_id == "human_hint_integration":
            return self.inquiry.execute_human_hint_integration(state, context)
        else:
            state.add_error(f"Unknown Inquiry pipeline: {pipeline_id}")
            return state
    
    def _execute_conduit(
        self,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute Conduit pipeline."""
        self._guard_experimental("Conduit", pipeline_id, state, context)
        if pipeline_id == "documentation":
            return self.conduit.execute_documentation(state, context)
        elif pipeline_id == "handoff_synthesis":
            return self.conduit.execute_handoff_synthesis(state, context)
        elif pipeline_id == "professional_writing":
            return self.conduit.execute_professional_writing(state, context)
        elif pipeline_id == "scholarly_writing":
            return self.conduit.execute_scholarly_writing(state, context)
        else:
            state.add_error(f"Unknown Conduit pipeline: {pipeline_id}")
            return state
