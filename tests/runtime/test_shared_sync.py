from pathlib import Path


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def test_shared_specs_are_in_sync():
    shared_root = Path("shared").resolve()
    assert shared_root.exists(), "shared directory missing"
    family_roots = [
        (Path("entrypoints") / "Forensics" / "shared").resolve(),
        (Path("entrypoints") / "Forge" / "shared").resolve(),
        (Path("entrypoints") / "Inquiry" / "shared").resolve(),
        (Path("entrypoints") / "Conduit" / "shared").resolve(),
    ]

    for copy_root in family_roots:
        assert copy_root.exists(), f"entrypoint shared copy missing: {copy_root}"

        for shared_file in shared_root.rglob("*"):
            if not shared_file.is_file():
                continue
            rel_path = shared_file.relative_to(shared_root)
            counterpart = copy_root / rel_path
            assert counterpart.exists(), f"Missing shared copy for {copy_root.name}/{rel_path}"
            assert _read_bytes(shared_file) == _read_bytes(counterpart), (
                f"Content mismatch for {copy_root.name}/{rel_path}"
            )
