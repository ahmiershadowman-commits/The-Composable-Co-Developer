"""
PrePipeline hook - validates entry conditions before pipeline execution.

See: docs/implementation/hook_and_interface_contract.md
"""

from hooks.context import HookContext, HookResult


def validate_entry_hook(context: HookContext) -> HookResult:
    """
    Validate pipeline entry conditions.
    
    Checks:
    - Pipeline exists in registry
    - Entry conditions are satisfied
    - Required context is present
    
    Args:
        context: Hook context with pipeline info
        
    Returns:
        HookResult with continue_execution=False if validation fails
    """
    pipeline_id = context.pipeline_id
    
    # Validate pipeline format
    if "/" not in pipeline_id:
        return HookResult.halt(
            f"Invalid pipeline format: {pipeline_id}. Expected 'Family/pipeline_id'"
        )
    
    family, pipeline_name = pipeline_id.split("/", 1)
    
    # Validate family
    valid_families = ["Forensics", "Forge", "Inquiry", "Conduit"]
    if family not in valid_families:
        return HookResult.halt(
            f"Unknown family: {family}. Valid families: {valid_families}"
        )
    
    # Validate context has required fields
    if family == "Forensics" and pipeline_name == "project_mapping" and "scope" not in context.context:
        return HookResult.halt(
            f"Forensics pipeline requires 'scope' in context"
        )
    
    if family == "Forge":
        if pipeline_name == "development" and "problem" not in context.context:
            return HookResult.halt(
                f"Forge pipeline requires 'problem' in context"
            )
        if pipeline_name == "coding" and not any(
            key in context.context for key in ("problem", "change_type", "affected_files")
        ):
            return HookResult.halt(
                "Forge/coding requires one of 'problem', 'change_type', or 'affected_files' in context"
            )
        if pipeline_name == "testing" and not any(
            key in context.context for key in ("test_scope", "problem")
        ):
            return HookResult.halt(
                "Forge/testing requires 'test_scope' or 'problem' in context"
            )
        if pipeline_name == "refactor" and "problem" not in context.context:
            return HookResult.halt(
                "Forge/refactor requires 'problem' in context"
            )
    
    # Check for state errors before starting
    if context.state.errors:
        return HookResult.halt(
            f"Cannot start pipeline with existing errors: {context.state.errors}"
        )
    
    return HookResult.success()
