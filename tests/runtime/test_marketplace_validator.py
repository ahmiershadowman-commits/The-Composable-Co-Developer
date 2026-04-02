from pathlib import Path

from tools.validate_marketplace import validate_marketplace


def test_marketplace_versions_and_paths_sync():
    repo_root = Path(__file__).resolve().parents[2]
    errors = validate_marketplace(repo_root)
    assert not errors, f"Marketplace validation failed: {errors}"
