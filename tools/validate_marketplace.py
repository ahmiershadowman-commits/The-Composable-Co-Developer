"""
Validate the Claude Code marketplace catalog.

Ensures every plugin source, command, and agent path exists and the declared version
matches the plugin manifest at that source.
"""

import json
from pathlib import Path
from typing import List


def validate_marketplace(repo_root: Path) -> List[str]:
    errors: List[str] = []
    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"

    if not marketplace_path.exists():
        errors.append("marketplace.json missing")
        return errors

    data = json.loads(marketplace_path.read_text(encoding="utf-8"))
    base_dir = marketplace_path.parent

    for plugin in data.get("plugins", []):
        name = plugin.get("name", "<unnamed>")
        source = plugin.get("source")
        declared_version = plugin.get("version")

        if not source:
            errors.append(f"{name}: missing source entry")
            continue

        plugin_path = (base_dir / source).resolve()
        if not plugin_path.exists():
            errors.append(f"{name}: plugin source not found at {plugin_path}")
            continue

        manifest_path = plugin_path / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            errors.append(f"{name}: plugin manifest not found at {manifest_path}")
            continue

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        actual_version = manifest.get("version")

        if declared_version != actual_version:
            errors.append(
                f"{name}: version mismatch (catalog {declared_version!r}, manifest {actual_version!r})"
            )

        for rel_path in plugin.get("commands", []):
            command_path = (base_dir / rel_path).resolve()
            if not command_path.exists():
                errors.append(f"{name}: command path not found at {command_path}")

        for rel_path in plugin.get("agents", []):
            agent_path = (base_dir / rel_path).resolve()
            if not agent_path.exists():
                errors.append(f"{name}: agent path not found at {agent_path}")

    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    issues = validate_marketplace(root)
    if issues:
        print("Marketplace validation failed:")
        for item in issues:
            print(f"- {item}")
        raise SystemExit(1)
    print("Marketplace validation passed")


if __name__ == "__main__":
    main()
