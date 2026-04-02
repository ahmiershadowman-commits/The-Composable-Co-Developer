#!/usr/bin/env bash
# run_pipeline.sh - Portable pipeline runner for the Composable Co-Developer plugin.
#
# Usage:
#   bash "${CLAUDE_PLUGIN_ROOT}/scripts/run_pipeline.sh" <Family> <pipeline_id> "<primary input>" [output_dir]
#
# Optional environment variables:
#   EXPERIMENTAL_APPROVAL_JSON   Inline JSON or a path to a JSON file for experimental pipelines.
#   RENDER_RUNTIME_REPORT=1      Render an HTML report after execution.
#   REQUIRE_MCP=name            Repeatable by invoking the script separately or pass --require-mcp later.

set -euo pipefail

FAMILY="${1:-}"
PIPELINE="${2:-}"
PRIMARY_INPUT="${3:-}"
OUTPUT_DIR="${4:-$(pwd)/runtime_output}"

if [[ -z "$FAMILY" || -z "$PIPELINE" ]]; then
  echo "Usage: run_pipeline.sh <Family> <pipeline_id> "<primary input>" [output_dir]" >&2
  exit 1
fi

if [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
  PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
else
  PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

resolve_runner() {
  local family="$1"
  if [[ -f "${PLUGIN_ROOT}/run.py" && "$(basename "${PLUGIN_ROOT}")" == "$family" ]]; then
    printf '%s' "${PLUGIN_ROOT}/run.py"
    return 0
  fi
  if [[ -f "${PLUGIN_ROOT}/../${family}/run.py" ]]; then
    printf '%s' "$(cd "${PLUGIN_ROOT}/../${family}" && pwd)/run.py"
    return 0
  fi
  if [[ -f "${PLUGIN_ROOT}/entrypoints/${family}/run.py" ]]; then
    printf '%s' "${PLUGIN_ROOT}/entrypoints/${family}/run.py"
    return 0
  fi
  return 1
}

case "$FAMILY" in
  Forensics)
    ARG_NAME="--scope"
    ;;
  Forge)
    ARG_NAME="--problem"
    ;;
  Inquiry)
    ARG_NAME="--question"
    ;;
  Conduit)
    ARG_NAME="--content"
    ;;
  *)
    echo "ERROR: Unknown family '$FAMILY'. Must be one of: Forensics Forge Inquiry Conduit" >&2
    exit 1
    ;;
esac

RUNNER="$(resolve_runner "$FAMILY")" || {
  echo "ERROR: Runner for $FAMILY not found from plugin root $PLUGIN_ROOT" >&2
  exit 1
}

mkdir -p "$OUTPUT_DIR"

CMD=(python "$RUNNER" --pipeline "$PIPELINE" "$ARG_NAME" "$PRIMARY_INPUT" --output "$OUTPUT_DIR" --project "$(pwd)")

if [[ -n "${EXPERIMENTAL_APPROVAL_JSON:-}" ]]; then
  CMD+=(--approval-json "$EXPERIMENTAL_APPROVAL_JSON")
fi

if [[ "${RENDER_RUNTIME_REPORT:-0}" == "1" ]]; then
  CMD+=(--render-report)
fi

if [[ -n "${REQUIRE_MCP:-}" ]]; then
  CMD+=(--require-mcp "$REQUIRE_MCP")
fi

if [[ "${CONNECT_ALL_MCP:-0}" == "1" ]]; then
  CMD+=(--connect-all-mcp)
fi

echo "Running ${FAMILY}/${PIPELINE}"
echo "Primary input: ${PRIMARY_INPUT}"
echo "Output: ${OUTPUT_DIR}"
echo ""

"${CMD[@]}"
