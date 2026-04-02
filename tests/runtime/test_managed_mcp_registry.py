from pathlib import Path

from runtime.mcp.registry import ManagedMCPRegistry


def test_managed_mcp_registry_loads_definitions():
    registry = ManagedMCPRegistry(Path("managed-mcp.json"))
    definitions = registry.load()

    assert "github-managed" in definitions
    assert "jira-managed" in definitions


def test_managed_mcp_registry_reports_missing_env_vars():
    registry = ManagedMCPRegistry(Path("managed-mcp.json"))
    registry.load()

    issues = registry.validate_env()

    assert any("github-managed" in issue for issue in issues)
