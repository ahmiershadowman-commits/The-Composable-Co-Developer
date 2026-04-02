"""
Guard script for PreToolUse hooks to block destructive shell commands or secrets exposure.

Reads JSON input (tool/command) from stdin and emits a HookResult-style JSON object.
"""

import json
import os
import re
import sys
from pathlib import Path

PATTERNS = [
    re.compile(r"\brm\s+-rf\b", re.IGNORECASE),
    re.compile(r"\bmkfs\b", re.IGNORECASE),
    re.compile(r"\bshutdown\b|\breboot\b", re.IGNORECASE),
    re.compile(r"\bgit\s+push\s+--force\b", re.IGNORECASE),
]
SECRET_PATTERNS = [
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
]


def _read_payload():
    """Read JSON payload from stdin or env vars."""
    if not sys.stdin or sys.stdin.isatty():
        return {}
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def _match_patterns(text, patterns):
    return any(p.search(text) for p in patterns)


def _extract_command(payload):
    if "command" in payload:
        return payload["command"]
    if "input" in payload:
        return payload["input"]
    return os.environ.get("CLAUDE_COMMAND", "")


def build_result(continue_execution, message=None):
    return {"continue_execution": continue_execution, "error_message": message}


def main():
    payload = _read_payload()
    tool = payload.get("tool", "").lower()
    command_text = _extract_command(payload)

    if _match_patterns(command_text, PATTERNS):
        print(json.dumps(build_result(False, "Destructive command blocked by guard.")))
        sys.exit(0)

    if tool in {"shell", "bash", "pwsh"} and _match_patterns(command_text, SECRET_PATTERNS):
        print(json.dumps(build_result(False, "Command references secrets; confirm intent before proceeding.")))
        sys.exit(0)

    print(json.dumps(build_result(True)))


if __name__ == "__main__":
    main()
