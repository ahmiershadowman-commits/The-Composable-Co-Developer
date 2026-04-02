from pathlib import Path


def test_unresolveds_schema_exists():
    schema_path = Path("runtime/schemas/artifacts/unresolveds_and_risks.yaml")
    assert schema_path.exists()


def test_taskboard_manifest_exists():
    manifest_path = Path("docs/implementation/taskboard_manifest.yaml")
    assert manifest_path.exists()
