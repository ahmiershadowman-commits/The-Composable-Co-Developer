from pathlib import Path


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def test_runtime_mirrors_are_in_sync():
    runtime_root = Path("runtime").resolve()
    assert runtime_root.exists(), "runtime directory missing"

    family_roots = [
        (Path("entrypoints") / "Forensics" / "runtime").resolve(),
        (Path("entrypoints") / "Forge" / "runtime").resolve(),
        (Path("entrypoints") / "Inquiry" / "runtime").resolve(),
        (Path("entrypoints") / "Conduit" / "runtime").resolve(),
    ]

    for copy_root in family_roots:
        assert copy_root.exists(), f"entrypoint runtime copy missing: {copy_root}"

        for runtime_file in runtime_root.rglob("*"):
            if not runtime_file.is_file():
                continue
            rel_path = runtime_file.relative_to(runtime_root)
            if "__pycache__" in rel_path.parts:
                continue
            counterpart = copy_root / rel_path
            assert counterpart.exists(), f"Missing runtime copy for {copy_root.name}/{rel_path}"
            assert _read_bytes(runtime_file) == _read_bytes(counterpart), (
                f"Content mismatch for {copy_root.name}/{rel_path}"
            )
