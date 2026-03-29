"""
Runtime dispatcher for pipeline execution.

Integrates family executors with the runtime spine
to execute actual pipeline phases.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from runtime.state.models import ExecutionState, FamilyType
from runtime.registry.loader import SpecIndex
from runtime.artifacts.writer import ArtifactWriter

# Import family executors
from entrypoints.Forensics.executors import ForensicsExecutor
from entrypoints.Forge.executors import ForgeExecutor
from entrypoints.Inquiry.executors import InquiryExecutor
from entrypoints.Conduit.executors import ConduitExecutor


# Experimental pipelines that are not available for production use.
# These are parked pending empirical validation.
EXPERIMENTAL_PIPELINES = {
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

    def _guard_experimental(self, family_name: str, pipeline_id: str) -> None:
        """
        Raise ExperimentalPipelineError if the pipeline is marked experimental.

        Call at the top of each _execute_* method.
        """
        blocked = EXPERIMENTAL_PIPELINES.get(family_name, set())
        if pipeline_id in blocked:
            raise ExperimentalPipelineError(
                f"'{pipeline_id}' is an experimental pipeline and is not available for use. "
                f"Experimental pipelines are parked pending empirical validation."
            )

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
        if family == FamilyType.FORENSICS:
            return self._execute_forensics(pipeline_id, state, context)
        elif family == FamilyType.FORGE:
            return self._execute_forge(pipeline_id, state, context)
        elif family == FamilyType.INQUIRY:
            return self._execute_inquiry(pipeline_id, state, context)
        elif family == FamilyType.CONDUIT:
            return self._execute_conduit(pipeline_id, state, context)
        else:
            state.add_error(f"Unknown family: {family}")
            return state
    
    def _execute_forensics(
        self,
        pipeline_id: str,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute Forensics pipeline."""
        self._guard_experimental("Forensics", pipeline_id)
        if pipeline_id == "project_mapping":
            return self.forensics.execute_project_mapping(state, context)
        elif pipeline_id == "defragmentation":
            return self.forensics.execute_defragmentation(state, context)
        elif pipeline_id == "documentation_audit":
            return self.forensics.execute_documentation_audit(state, context)
        elif pipeline_id == "anomaly_disambiguation":
            return self.forensics.execute_anomaly_disambiguation(state, context)
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
        self._guard_experimental("Forge", pipeline_id)
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
        self._guard_experimental("Inquiry", pipeline_id)
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
        self._guard_experimental("Conduit", pipeline_id)
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
