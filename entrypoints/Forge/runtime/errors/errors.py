"""
Runtime error types for the composable co-developer.
"""


class RuntimeError(Exception):
    """Base runtime error."""
    pass


class TargetResolutionError(RuntimeError):
    """Error resolving a target."""
    pass


class TransitionError(RuntimeError):
    """Error during state transition."""
    pass


class RegistryError(RuntimeError):
    """Error loading or indexing specs."""
    pass


class PipelineError(RuntimeError):
    """Error during pipeline execution."""
    pass


class ValidationError(RuntimeError):
    """Error during validation."""
    pass
