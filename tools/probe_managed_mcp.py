"""Probe managed MCP endpoints and emit a session report."""

import argparse
from pathlib import Path

from runtime.mcp.registry import ManagedMCPRegistry
from runtime.mcp.session_host import ManagedMCPSessionHost


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe managed MCP endpoints.")
    parser.add_argument(
        "--config",
        default="managed-mcp.json",
        help="Path to managed-mcp.json",
    )
    parser.add_argument(
        "--output",
        default="runtime_output/_reports/managed_mcp_sessions.yaml",
        help="Where to write the session report",
    )
    parser.add_argument(
        "--name",
        action="append",
        dest="names",
        help="Specific managed MCP name(s) to probe; defaults to all",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=2.0,
        help="Per-endpoint network timeout",
    )
    args = parser.parse_args()

    registry = ManagedMCPRegistry(Path(args.config))
    registry.load()
    host = ManagedMCPSessionHost(registry)
    host.connect_many(args.names, timeout_seconds=args.timeout_seconds)
    report_path = host.write_report(Path(args.output))
    print(f"Wrote managed MCP report to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
