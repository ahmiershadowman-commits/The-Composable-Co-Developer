"""
PostPipeline hook - reviews pipeline output for quality issues.

See: docs/implementation/hook_and_interface_contract.md
"""

from hooks.context import HookContext, HookResult


def review_output_hook(context: HookContext) -> HookResult:
    """
    Review pipeline output for quality and completeness.
    
    Checks:
    - Required artifacts were produced
    - Artifacts have valid structure
    - Route recommendation is present and valid
    
    Args:
        context: Hook context with pipeline state
        
    Returns:
        HookResult with warnings or errors
    """
    artifacts = context.state.artifacts
    pipeline_id = context.pipeline_id
    
    # Check for route_recommendation (required for all pipelines)
    if "route_recommendation" not in artifacts:
        return HookResult(
            continue_execution=True,
            error_message=f"Missing route_recommendation in {pipeline_id}",
            modifications={"quality_warning": "Missing route recommendation"},
        )
    
    # Check artifact count (should have produced something)
    if len(artifacts) < 2:  # At least route_recommendation + one other
        return HookResult(
            continue_execution=True,
            error_message=f"Pipeline {pipeline_id} produced minimal artifacts",
            modifications={"quality_warning": "Minimal artifact output"},
        )
    
    # Family-specific checks
    family = context.state.current_family.value
    
    if family == "Forensics":
        return _check_forensics_artifacts(context)
    elif family == "Forge":
        return _check_forge_artifacts(artifacts, pipeline_id)
    elif family == "Inquiry":
        return _check_inquiry_artifacts(artifacts, pipeline_id)
    elif family == "Conduit":
        return _check_conduit_artifacts(artifacts, pipeline_id)
    
    return HookResult.success()


def _check_forensics_artifacts(context: HookContext) -> HookResult:
    """Check Forensics-specific required artifacts."""
    artifacts = context.state.artifacts
    pipeline_id = context.pipeline_id
    # All Forensics pipelines should produce trust-related artifacts
    if "trust_assessment" not in artifacts and context.state.trust_assessment is None:
        return HookResult(
            continue_execution=True,
            error_message=f"Forensics pipeline {pipeline_id} missing trust assessment",
            modifications={"quality_warning": "Missing trust assessment"},
        )
    return HookResult.success()


def _check_forge_artifacts(artifacts: dict, pipeline_id: str) -> HookResult:
    """Check Forge-specific required artifacts."""
    # Forge should produce change-related artifacts
    change_artifacts = ["change_plan", "work_plan", "test_strategy"]
    has_change_artifact = any(k in artifacts for k in change_artifacts)
    
    if not has_change_artifact:
        return HookResult(
            continue_execution=True,
            error_message=f"Forge pipeline {pipeline_id} produced no change artifacts",
            modifications={"quality_warning": "Missing change artifacts"},
        )
    return HookResult.success()


def _check_inquiry_artifacts(artifacts: dict, pipeline_id: str) -> HookResult:
    """Check Inquiry-specific required artifacts."""
    # Inquiry should produce research/findings artifacts
    research_artifacts = ["research_findings", "hypothesis_ledger", "analysis_report"]
    has_research_artifact = any(k in artifacts for k in research_artifacts)
    
    if not has_research_artifact:
        return HookResult(
            continue_execution=True,
            error_message=f"Inquiry pipeline {pipeline_id} produced no research artifacts",
            modifications={"quality_warning": "Missing research artifacts"},
        )
    return HookResult.success()


def _check_conduit_artifacts(artifacts: dict, pipeline_id: str) -> HookResult:
    """Check Conduit-specific required artifacts."""
    # Conduit should produce documentation/synthesis artifacts
    doc_artifacts = ["documentation", "synthesis_report", "handoff_document"]
    has_doc_artifact = any(k in artifacts for k in doc_artifacts)
    
    if not has_doc_artifact:
        return HookResult(
            continue_execution=True,
            error_message=f"Conduit pipeline {pipeline_id} produced no documentation artifacts",
            modifications={"quality_warning": "Missing documentation artifacts"},
        )
    return HookResult.success()
