"""
Managed MCP registry.

Loads and validates the team-managed MCP template shipped with the marketplace.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ManagedMCPDefinition:
    """Structured representation of one managed MCP entry."""

    name: str
    transport: str
    url: str
    env: Dict[str, str] = field(default_factory=dict)
    notes: str = ""

    def required_env_vars(self) -> List[str]:
        """Return required env var names for this MCP definition."""
        return list(self.env.keys())

    def missing_env_vars(self) -> List[str]:
        """Return required env vars that are not currently set."""
        return [name for name in self.required_env_vars() if not os.environ.get(name)]


class ManagedMCPRegistry:
    """Loads managed MCP definitions from a JSON file."""

    def __init__(self, config_path: Path):
        self.config_path = Path(config_path)
        self._definitions: Dict[str, ManagedMCPDefinition] = {}

    def load(self) -> Dict[str, ManagedMCPDefinition]:
        """Load and validate the managed MCP config."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Managed MCP config missing: {self.config_path}")

        raw = json.loads(self.config_path.read_text(encoding="utf-8"))
        definitions: Dict[str, ManagedMCPDefinition] = {}
        for item in raw:
            definition = ManagedMCPDefinition(
                name=item["name"],
                transport=item["transport"],
                url=item["url"],
                env=item.get("env", {}),
                notes=item.get("notes", ""),
            )
            definitions[definition.name] = definition

        self._definitions = definitions
        return definitions

    def get(self, name: str) -> Optional[ManagedMCPDefinition]:
        """Get a single managed MCP definition by name."""
        return self._definitions.get(name)

    def names(self) -> List[str]:
        """Return loaded managed MCP names."""
        return sorted(self._definitions.keys())

    def validate_env(self) -> List[str]:
        """Validate env requirements for all loaded definitions."""
        issues: List[str] = []
        for definition in self._definitions.values():
            missing = definition.missing_env_vars()
            if missing:
                issues.append(
                    f"{definition.name}: missing env vars {', '.join(sorted(missing))}"
                )
        return issues
