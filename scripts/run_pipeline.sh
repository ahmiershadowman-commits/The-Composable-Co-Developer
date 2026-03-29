#!/usr/bin/env bash
# run_pipeline.sh — Portable pipeline runner for the Composable Co-Developer plugin.
#
# Usage:
#   bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" <Family> <pipeline_id> "<scope>" [output_dir]
#
# Arguments:
#   Family       — Forensics | Forge | Inquiry | Conduit
#   pipeline_id  — e.g. project_mapping, coding, research, documentation
#   scope        — description of what is being analyzed/built (quoted)
#   output_dir   — optional; defaults to ./runtime_output in the caller's cwd
#
# ${CLAUDE_PLUGIN_ROOT} is injected by Claude Code when the plugin is active.
# Inside this script it resolves to the plugin installation directory.

set -euo pipefail

FAMILY="${1:-}"
PIPELINE="${2:-}"
SCOPE="${3:-}"
OUTPUT_DIR="${4:-$(pwd)/runtime_output}"

if [[ -z "$FAMILY" || -z "$PIPELINE" ]]; then
  echo "Usage: run_pipeline.sh <Family> <pipeline_id> \"<scope>\" [output_dir]" >&2
  exit 1
fi

# Resolve plugin root — prefer the injected env variable, fall back to script location
if [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
  PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
else
  PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

# Map family name to run.py location and its argument name
case "$FAMILY" in
  Forensics)
    RUNNER="${PLUGIN_ROOT}/entrypoints/Forensics/run.py"
    ARG_NAME="--scope"
    PIPELINES="project_mapping|defragmentation|documentation_audit|anomaly_disambiguation"
    ;;
  Forge)
    RUNNER="${PLUGIN_ROOT}/entrypoints/Forge/run.py"
    ARG_NAME="--problem"
    PIPELINES="development|coding|testing|refactor"
    ;;
  Inquiry)
    RUNNER="${PLUGIN_ROOT}/entrypoints/Inquiry/run.py"
    ARG_NAME="--question"
    PIPELINES="research|hypothesis_generation|data_analysis|formalization|mathematics"
    ;;
  Conduit)
    RUNNER="${PLUGIN_ROOT}/entrypoints/Conduit/run.py"
    ARG_NAME="--content"
    PIPELINES="documentation|handoff_synthesis|professional_writing|scholarly_writing"
    ;;
  *)
    echo "ERROR: Unknown family '$FAMILY'. Must be one of: Forensics Forge Inquiry Conduit" >&2
    exit 1
    ;;
esac

if [[ ! -f "$RUNNER" ]]; then
  echo "ERROR: Runner not found at $RUNNER" >&2
  echo "Ensure the plugin was installed from the full bundle including the Python runtime." >&2
  exit 1
fi

# Guard experimental pipelines
EXPERIMENTAL="label_shift_correction|introspection_audit|prompt_order_optimization|human_hint_integration"
if echo "$PIPELINE" | grep -qE "^(${EXPERIMENTAL})$"; then
  echo "ERROR: '$PIPELINE' is an experimental pipeline and is not available for use." >&2
  echo "Experimental pipelines are parked pending empirical validation." >&2
  exit 2
fi

mkdir -p "$OUTPUT_DIR"

echo "Running ${FAMILY}/${PIPELINE}"
echo "Scope: ${SCOPE}"
echo "Output: ${OUTPUT_DIR}"
echo ""

python3 "$RUNNER" \
  --pipeline "$PIPELINE" \
  $ARG_NAME "$SCOPE" \
  --output "$OUTPUT_DIR" \
  --project "$(pwd)"
