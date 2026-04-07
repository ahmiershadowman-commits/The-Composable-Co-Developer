# Deploy Checklist: The Composable Co-Developer

Use this checklist before every release to `main`. Even routine version bumps.

> **Platform note:** CI runs on `windows-latest` (Python 3.10, 3.11, 3.12 matrix). All commands below assume Windows unless noted. The mirror sync step is the most common source of silent failures — do not skip it.

---

## Pre-Deploy

### Code quality

- [ ] All tests passing locally on all three Python versions
  ```
  python -m pytest tests/ -v --tb=short
  ```
- [ ] Vertical slice passes (end-to-end pipeline execution check)
  ```
  python tools/run_vertical_slice.py
  ```
- [ ] Bundle validated (spec/executor alignment check)
  ```
  python tools/validate_bundle.py
  ```
- [ ] No known critical bugs in this release

### Mirror sync (mandatory — most common failure point)

- [ ] Runtime mirrors are in sync with `runtime/` source
  ```
  python -c "
  import shutil
  from pathlib import Path
  runtime_root = Path('runtime')
  for ep in ['Forensics', 'Forge', 'Inquiry', 'Conduit']:
      copy_root = Path(f'entrypoints/{ep}/runtime')
      for f in runtime_root.rglob('*'):
          if not f.is_file() or '__pycache__' in f.parts:
              continue
          dest = copy_root / f.relative_to(runtime_root)
          dest.parent.mkdir(parents=True, exist_ok=True)
          if not dest.exists() or dest.read_bytes() != f.read_bytes():
              shutil.copy2(f, dest)
  print('Runtime mirrors synced')
  "
  ```
- [ ] Shared mirrors are in sync with `shared/` source
  ```
  python -c "
  import shutil
  from pathlib import Path
  shared_root = Path('shared')
  for ep in ['Forensics', 'Forge', 'Inquiry', 'Conduit']:
      copy_root = Path(f'entrypoints/{ep}/shared')
      for f in shared_root.rglob('*'):
          if not f.is_file() or '__pycache__' in f.parts:
              continue
          dest = copy_root / f.relative_to(shared_root)
          dest.parent.mkdir(parents=True, exist_ok=True)
          if not dest.exists() or dest.read_bytes() != f.read_bytes():
              shutil.copy2(f, dest)
  print('Shared mirrors synced')
  "
  ```
- [ ] Mirror sync tests pass (confirms CI will pass)
  ```
  python -m pytest tests/runtime/test_runtime_mirror_sync.py tests/runtime/test_shared_sync.py -v
  ```

### Architecture gates (from BUILD_CONTRACT.md)

- [ ] **Gate 1 — Grammar:** `runtime/schemas/pipeline.yaml` and `runtime/methodology/target_grammar.yaml` are unchanged or changes are deliberate
- [ ] **Gate 2 — Inventory:** No ghost pipelines in selector scopes or route maps
  - Check: every pipeline in `entrypoints/*/pipelines/` appears in the family `family_route_map.yaml`
- [ ] **Gate 3 — Family coherence:** Experimental pipelines remain explicitly marked in `EXPERIMENTAL_PIPELINES` dict in `dispatcher.py`
- [ ] **Gate 4 — Target resolution:** Every pivot target, route map entry, and selector target resolves via `TargetResolver`
- [ ] **Gate 5 — Semantic architecture:** Forensics/Forge/Inquiry/Conduit/Trace/Lever/Residue roles unchanged

### Evaluator registry consistency

- [ ] All evaluator IDs in `shared/Lever/evaluator_registry.yaml` have matching dispatch handlers in `runtime/lever/escalation.py`
- [ ] All evaluator IDs referenced in motif YAML files (`shared/motifs/*.yaml`) match registry entries exactly (previous bug: `discrimination_evaluator` vs `discriminator_evaluator`)

### Skill documentation consistency

- [ ] Forge SKILL.md descriptions are identical across `skills/forge/SKILL.md` and all four `entrypoints/*/skills/forge/SKILL.md` files
- [ ] Inquiry SKILL.md experimental pipeline status is identical across all five files (`approval required`, not `not available`)
- [ ] Any new motifs added to `shared/motifs/registry.yaml` have corresponding YAML files and are mirrored to all entrypoints

### GitHub Actions

- [ ] CI workflow (`.github/workflows/tests.yml`) is unchanged or updated intentionally
- [ ] CI is green on the release branch (all three Python versions: 3.10, 3.11, 3.12)
- [ ] No skipped tests that should be passing (currently 1 expected skip — confirm it is the same one)

### Code review

- [ ] PR reviewed and approved
- [ ] All audit findings from the last superpowers/plugin review addressed
- [ ] No `# TODO` or `# FIXME` markers introduced in this release that aren't tracked

### Rollback plan

- [ ] Rollback commit identified (last known-good SHA: `e938617`)
- [ ] Rollback steps documented:
  ```
  git revert HEAD
  # or
  git checkout e938617 -- <specific file>
  ```

---

## Deploy

### GitHub release

- [ ] Version bumped in `.claude-plugin/plugin.json` (and all four `entrypoints/*/plugin.json` files)
- [ ] Version consistent across all manifests (check: `grep -r '"version"' .claude-plugin/ entrypoints/*/`.claude-plugin/`)
- [ ] Changelog / release notes written
- [ ] Tag created: `git tag v1.x.x && git push origin v1.x.x`
- [ ] GitHub Release created from tag (include changelog)

### Plugin distribution (if publishing to marketplace)

- [ ] `marketplace.json` paths all resolve to existing entrypoints
- [ ] Plugin zip or bundle validated: `python tools/validate_marketplace.py`
- [ ] README reflects current version and any new features

---

## Post-Deploy

- [ ] CI green on `main` after merge (confirm all three Python versions pass)
- [ ] GitHub Actions run completed without warnings
- [ ] Mirror sync tests still passing on `main`
- [ ] Close related issues/tickets
- [ ] Notify any downstream users of breaking changes (if any)

---

## Rollback Triggers

Roll back immediately if any of the following are true after deploy:

- Mirror sync tests fail on `main`
- `validate_bundle.py` fails on `main`
- Any evaluator in `escalation.py` falls to `_evaluate_generic` for a mapped evaluator ID
- Trust verification hook (`PreToolUse/Bash`) stops firing for Forge/Inquiry invocations
- `trigger_ownership_hook` is not registered for `PRE_TRANSITION` (check dispatcher `_build_hook_registry`)
- Vertical slice produces an executor `AttributeError` (indicates missing helper method)

---

## Known Acceptable Skips

| Skip | Reason | Safe to ship? |
|---|---|---|
| 1 test skipped in pytest suite | Platform-conditional test (identified in test file) | Yes, if same test as before |

---

## Checklist Owner

Ash — confirm all items before tagging release.
