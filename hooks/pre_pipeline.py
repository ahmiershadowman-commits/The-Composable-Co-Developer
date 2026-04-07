"""
PrePipeline hook - validates entry conditions before pipeline execution.

See: docs/implementation/hook_and_interface_contract.md
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from hooks.context import HookContext, HookResult

# ---------------------------------------------------------------------------
# Pipeline spec loader
# ---------------------------------------------------------------------------

_ENTRYPOINTS_ROOT = Path(__file__).parent.parent / "entrypoints"


def _load_pipeline_spec(family: str, pipeline_name: str) -> Optional[Dict[str, Any]]:
    """Load pipeline YAML spec from the entrypoints directory tree.

    Searches: entrypoints/<Family>/pipelines/<pipeline_name>/pipeline.yaml
    Falls back to: entrypoints/<Family>/pipelines/<pipeline_name>.yaml
    """
    base = _ENTRYPOINTS_ROOT / family / "pipelines"
    candidates = [
        base / pipeline_name / "pipeline.yaml",
        base / f"{pipeline_name}.yaml",
    ]
    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    return yaml.safe_load(fh)
            except Exception:
                return None
    return None


# ---------------------------------------------------------------------------
# Entry condition evaluation
# ---------------------------------------------------------------------------

# Conditions that map directly to required context keys.
# If a condition ID matches a key here, the key must be truthy in context.
_CONDITION_TO_CONTEXT_KEY: Dict[str, str] = {
    # Forensics
    "project_scope_is_defined": "scope",
    "a_mapping_target_is_specified": "scope",
    # Forge — note: "grounded enough for build work" operationally requires a problem statement
    "a_buildable_problem_is_defined": "problem",
    "project_state_is_grounded_enough_for_build_work": "problem",
    "a_coding_change_is_scoped": "change_type",
    "test_scope_is_defined_or_implied_by_state": "test_scope",
    "a_refactor_target_is_identified": "problem",
    # Inquiry
    "a_question_requiring_evidence_workup_is_stated": "question",
    # Conduit
    "a_documentation_gap_or_target_is_identified": "doc_target",
    "handoff_state_exists_in_artifacts": "artifacts",
    "a_writing_task_is_scoped": "topic",
    "a_scholarly_writing_task_is_scoped": "topic",
}

# Conditions that are explicitly fatal — if they appear in entry_conditions
# and the context signals violation, halt.
_BLOCKING_NEGATION_KEYS: Dict[str, str] = {
    "ground_truth_is_sufficiently_stable_or_forensics_has_bounded_the_surface": "ground_truth_unstable",
    "no_active_trust_collapse": "trust_collapsed",
    "state_surface_is_not_in_trust_collapse": "trust_collapsed",
}


def _evaluate_entry_conditions(
    conditions: List[str],
    context: Dict[str, Any],
    state_artifacts: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """Evaluate pipeline entry_conditions against context.

    Returns (all_satisfied, list_of_violation_messages).

    Strategy:
    - If a condition maps to a context key via _CONDITION_TO_CONTEXT_KEY,
      verify that key is truthy in context.
    - If a condition appears in _BLOCKING_NEGATION_KEYS, verify the
      corresponding blocker key is NOT truthy.
    - Purely semantic conditions (no mapping) pass silently — they are
      intent-level preconditions enforced by the caller, not the hook.
    """
    violations: List[str] = []

    for condition in conditions:
        # Direct context-key requirement
        if condition in _CONDITION_TO_CONTEXT_KEY:
            required_key = _CONDITION_TO_CONTEXT_KEY[condition]
            if required_key == "artifacts":
                # Special case: check state artifacts instead of context
                if not state_artifacts:
                    violations.append(
                        f"Entry condition '{condition}' requires artifacts in state, but none found"
                    )
            elif not context.get(required_key):
                violations.append(
                    f"Entry condition '{condition}' requires '{required_key}' in context"
                )

        # Blocking negation — explicit violation indicator
        elif condition in _BLOCKING_NEGATION_KEYS:
            blocker_key = _BLOCKING_NEGATION_KEYS[condition]
            if context.get(blocker_key) or state_artifacts.get(blocker_key):
                violations.append(
                    f"Entry condition '{condition}' is violated: '{blocker_key}' is set"
                )

        # Try a simple snake_case key match (condition itself as context key)
        elif condition.replace("-", "_") in context:
            val = context[condition.replace("-", "_")]
            if val is False:
                violations.append(
                    f"Entry condition '{condition}' is explicitly False in context"
                )

        # Semantic condition with no mapping — passes (intent-level, not programmatic)

    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# Hook entry point
# ---------------------------------------------------------------------------

def validate_entry_hook(context: HookContext) -> HookResult:
    """
    Validate pipeline entry conditions by loading the pipeline YAML spec
    and evaluating its entry_conditions against the provided context.

    Checks:
    - Pipeline ID format (Family/pipeline_name)
    - Family is recognised
    - State has no pre-existing errors
    - entry_conditions from pipeline YAML spec are satisfied
    """
    pipeline_id = context.pipeline_id

    # 1. Validate pipeline ID format
    if "/" not in pipeline_id:
        return HookResult.halt(
            f"Invalid pipeline format: '{pipeline_id}'. Expected 'Family/pipeline_id'"
        )

    family, pipeline_name = pipeline_id.split("/", 1)

    # 2. Validate family
    valid_families = {"Forensics", "Forge", "Inquiry", "Conduit"}
    if family not in valid_families:
        return HookResult.halt(
            f"Unknown family: '{family}'. Valid: {sorted(valid_families)}"
        )

    # 3. Check for pre-existing state errors
    if context.state.errors:
        return HookResult.halt(
            f"Cannot start pipeline '{pipeline_id}' with existing state errors: "
            f"{context.state.errors}"
        )

    # 4. Load pipeline spec and evaluate entry_conditions
    spec = _load_pipeline_spec(family, pipeline_name)

    if spec is None:
        # Spec not found — log a warning but don't hard-block; pipeline may be valid
        return HookResult.success(
            modifications={"entry_condition_warning": f"Pipeline spec not found for '{pipeline_id}'"}
        )

    entry_conditions: List[str] = spec.get("entry_conditions", [])

    if not entry_conditions:
        # No conditions declared — always passes
        return HookResult.success()

    all_satisfied, violations = _evaluate_entry_conditions(
        entry_conditions,
        context.context,
        context.state.artifacts,
    )

    if not all_satisfied:
        return HookResult.halt(
            f"Pipeline '{pipeline_id}' entry conditions not satisfied: "
            + "; ".join(violations)
        )

    return HookResult.success(
        modifications={
            "entry_conditions_checked": entry_conditions,
            "entry_conditions_satisfied": True,
        }
    )
