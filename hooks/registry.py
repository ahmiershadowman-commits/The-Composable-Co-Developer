"""
Hook registry for managing hook execution.

See: docs/implementation/hook_and_interface_contract.md
"""

from typing import Any, Callable, Dict, List, Optional
from enum import Enum

from hooks.context import HookContext, HookResult


class HookEvent(str, Enum):
    """Hook event types."""
    PRE_PIPELINE = "PrePipeline"
    POST_PIPELINE = "PostPipeline"
    PRE_PHASE = "PrePhase"
    POST_PHASE = "PostPhase"
    PRE_TRANSITION = "PreTransition"
    POST_TRANSITION = "PostTransition"
    PRE_ROUTE = "PreRoute"
    POST_ROUTE = "PostRoute"
    ON_ERROR = "OnError"
    ON_CHECKPOINT = "OnCheckpoint"


class HookType(str, Enum):
    """Hook implementation types."""
    COMMAND = "command"
    PROMPT = "prompt"
    AGENT = "agent"
    PYTHON = "python"


class HookRegistry:
    """
    Registry for managing hook execution.
    
    Hooks are executed in order of registration for each event.
    """
    
    def __init__(self):
        self._hooks: Dict[HookEvent, List[Callable]] = {
            event: [] for event in HookEvent
        }
    
    def register(
        self,
        event: HookEvent,
        hook_func: Callable[[HookContext], HookResult],
        priority: int = 0,
    ) -> None:
        """
        Register a hook for an event.
        
        Args:
            event: Hook event type
            hook_func: Hook function (HookContext -> HookResult)
            priority: Higher priority hooks run first (default 0)
        """
        self._hooks[event].append((priority, hook_func))
        # Sort by priority descending
        self._hooks[event].sort(key=lambda x: -x[0])
    
    def unregister(self, event: HookEvent, hook_func: Callable) -> bool:
        """
        Unregister a hook.
        
        Args:
            event: Hook event type
            hook_func: Hook function to remove
            
        Returns:
            True if hook was found and removed
        """
        hooks = self._hooks[event]
        for i, (_, func) in enumerate(hooks):
            if func == hook_func:
                hooks.pop(i)
                return True
        return False
    
    def execute(
        self,
        event: HookEvent,
        context: HookContext,
    ) -> HookResult:
        """
        Execute all hooks for an event.
        
        Args:
            event: Hook event type
            context: Hook context
            
        Returns:
            Combined result (first failure stops execution)
        """
        hooks = self._hooks[event]
        
        for _, hook_func in hooks:
            try:
                result = hook_func(context)
                
                if not result.continue_execution:
                    return result
                
                # Apply modifications to context
                self._apply_modifications(context, result.modifications)
                
            except Exception as e:
                return HookResult.halt(f"Hook {event.value} failed: {e}")
        
        return HookResult.success()
    
    def _apply_modifications(
        self,
        context: HookContext,
        modifications: Dict[str, Any],
    ) -> None:
        """Apply hook modifications to context."""
        # Hook can modify context.context but not state directly
        context.context.update(modifications.get("context", {}))
    
    def list_hooks(self, event: HookEvent) -> List[str]:
        """List registered hooks for an event."""
        return [f"priority={p}, func={f.__name__}" for p, f in self._hooks[event]]
    
    def clear(self, event: Optional[HookEvent] = None) -> None:
        """
        Clear hooks.
        
        Args:
            event: Specific event to clear, or None for all
        """
        if event is None:
            for e in HookEvent:
                self._hooks[e] = []
        else:
            self._hooks[event] = []
