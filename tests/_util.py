from __future__ import annotations
from pathlib import Path
import re
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

TARGET_PATTERN = re.compile(
    r'^(primitive:[\w_]+|operator:[\w_]+|evaluator:[\w_]+|method:[\w_]+|pipeline:[A-Za-z]+/[\w_]+|family:[A-Za-z]+|authority:(Trace|Lever|Residue)|forensics_reset)$'
)

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def pipeline_files():
    return list(REPO_ROOT.glob('entrypoints/*/pipelines/*/pipeline.yaml'))

def selector_files():
    return list(REPO_ROOT.glob('entrypoints/*/selector.route.yaml'))

def family_route_maps():
    return list(REPO_ROOT.glob('entrypoints/*/family_route_map.yaml'))

def all_yaml_files():
    return [p for p in REPO_ROOT.rglob('*.yaml') if p.is_file()]

def inventory():
    inv = {}
    for fam_dir in REPO_ROOT.glob('entrypoints/*'):
        if fam_dir.is_dir():
            inv[fam_dir.name] = sorted([p.parent.name for p in fam_dir.glob('pipelines/*/pipeline.yaml')])
    return inv

def primitive_ids():
    ids = set()
    for p in REPO_ROOT.glob('shared/primitives/*/*.yaml'):
        d = load_yaml(p)
        ids.add(d['id'])
    return ids

def operator_ids():
    ids = set()
    for p in REPO_ROOT.glob('shared/operators/*.yaml'):
        d = load_yaml(p)
        ids.add(d['id'])
    return ids

def evaluator_ids():
    d = load_yaml(REPO_ROOT / 'shared/Lever/evaluator_registry.yaml')
    return set(d.get('evaluators', {}).keys())

def collect_targets(obj):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'target' and isinstance(v, str):
                found.append(v)
            else:
                found.extend(collect_targets(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(collect_targets(item))
    return found
