"""Managed MCP session probing and reporting."""

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Dict, Iterable, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yaml

from runtime.mcp.registry import ManagedMCPDefinition, ManagedMCPRegistry


@dataclass
class ManagedMCPSession:
    """One attempted managed MCP session."""

    name: str
    transport: str
    url: str
    connected: bool
    latency_ms: Optional[int] = None
    status_code: Optional[int] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Return a serializable session payload."""
        return {
            "name": self.name,
            "transport": self.transport,
            "url": self.url,
            "connected": self.connected,
            "latency_ms": self.latency_ms,
            "status_code": self.status_code,
            "error": self.error,
        }


class ManagedMCPSessionHost:
    """Probe and report the health of managed MCP endpoints."""

    def __init__(self, registry: ManagedMCPRegistry):
        self.registry = registry
        self.sessions: Dict[str, ManagedMCPSession] = {}

    def connect(self, name: str, timeout_seconds: float = 2.0) -> ManagedMCPSession:
        """Attempt a lightweight connection probe for one managed MCP endpoint."""
        definition = self.registry.get(name)
        if definition is None:
            session = ManagedMCPSession(
                name=name,
                transport="unknown",
                url="",
                connected=False,
                error="Managed MCP definition not found",
            )
            self.sessions[name] = session
            return session

        missing_env = definition.missing_env_vars()
        if missing_env:
            session = ManagedMCPSession(
                name=definition.name,
                transport=definition.transport,
                url=definition.url,
                connected=False,
                error="Missing env vars: " + ", ".join(sorted(missing_env)),
            )
            self.sessions[name] = session
            return session

        if definition.transport not in {"http", "https"}:
            session = ManagedMCPSession(
                name=definition.name,
                transport=definition.transport,
                url=definition.url,
                connected=False,
                error=f"Unsupported transport: {definition.transport}",
            )
            self.sessions[name] = session
            return session

        started = perf_counter()
        request = Request(definition.url, headers={"User-Agent": "composable-runtime/1.1"})
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                latency_ms = int((perf_counter() - started) * 1000)
                session = ManagedMCPSession(
                    name=definition.name,
                    transport=definition.transport,
                    url=definition.url,
                    connected=200 <= response.status < 400,
                    latency_ms=latency_ms,
                    status_code=response.status,
                )
        except HTTPError as exc:
            session = ManagedMCPSession(
                name=definition.name,
                transport=definition.transport,
                url=definition.url,
                connected=False,
                status_code=exc.code,
                error=str(exc),
            )
        except URLError as exc:
            session = ManagedMCPSession(
                name=definition.name,
                transport=definition.transport,
                url=definition.url,
                connected=False,
                error=str(exc.reason),
            )

        self.sessions[definition.name] = session
        return session

    def connect_many(
        self,
        names: Optional[Iterable[str]] = None,
        timeout_seconds: float = 2.0,
    ) -> Dict[str, ManagedMCPSession]:
        """Probe a subset of managed MCP endpoints or all loaded definitions."""
        requested = list(names) if names is not None else self.registry.names()
        return {
            name: self.connect(name, timeout_seconds=timeout_seconds)
            for name in requested
        }

    def write_report(self, output_path: Path) -> Path:
        """Write the current session probe results to disk."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "sessions": [session.to_dict() for session in self.sessions.values()],
            "total": len(self.sessions),
            "connected": sum(1 for session in self.sessions.values() if session.connected),
        }
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        return path
