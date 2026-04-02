"""
Hook system for The Composable Co-Developer marketplace runtime.

Hooks allow external code to intercept and influence runtime execution at defined points.
See: docs/implementation/hook_and_interface_contract.md
"""

from hooks.context import HookContext, HookResult
from hooks.registry import HookRegistry
from hooks.pre_pipeline import validate_entry_hook
from hooks.post_pipeline import review_output_hook

__all__ = [
    "HookContext",
    "HookResult", 
    "HookRegistry",
    "validate_entry_hook",
    "review_output_hook",
]
