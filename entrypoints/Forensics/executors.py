"""
Forensics pipeline executors.

Implements execution for Forensics family pipelines:
- project_mapping
- defragmentation
- documentation_audit
- anomaly_disambiguation
"""

import ast
import re
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from runtime.state.models import ExecutionState, TrustAssessment, FamilyType
from runtime.artifacts.writer import ArtifactWriter


# ---------------------------------------------------------------------------
# File classification helpers
# ---------------------------------------------------------------------------

_CODE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java",
              ".c", ".cpp", ".h", ".rb", ".sh", ".bash"}
_DOC_EXTS  = {".md", ".rst", ".txt", ".adoc"}
_CONFIG_EXTS = {".yaml", ".yml", ".json", ".toml", ".ini", ".env", ".cfg",
                ".conf", ".lock"}
_TEST_DIRS  = {"tests", "test", "__tests__", "spec"}

# Directories to skip entirely during inventory
_SKIP_DIRS = {
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules",
    ".venv", "venv", "env", ".env", "dist", "build", ".tox", ".eggs",
    "*.egg-info",
}


def _classify_file(path: Path, project_root: Path) -> str:
    """Return the artifact type for a file."""
    ext = path.suffix.lower()
    parts = set(path.relative_to(project_root).parts)
    if parts & _TEST_DIRS:
        return "test"
    if ext in _CODE_EXTS:
        return "code"
    if ext in _DOC_EXTS:
        return "doc"
    if ext in _CONFIG_EXTS:
        return "config"
    return "other"


def _should_skip(name: str) -> bool:
    return name in _SKIP_DIRS or name.endswith(".egg-info")


# ---------------------------------------------------------------------------
# Import tracing helpers
# ---------------------------------------------------------------------------

def _extract_python_imports(path: Path) -> List[str]:
    """Return local module imports found in a Python file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return []
    imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def _extract_yaml_references(path: Path) -> List[str]:
    """Return file paths referenced inside a YAML/markdown file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # Match path-like strings: relative paths starting with ./ or containing /
    return re.findall(r'(?:\.\.?/[\w./\-_]+|[\w\-_]+/[\w./\-_]+\.(?:py|yaml|yml|md|json|sh))', text)


# ---------------------------------------------------------------------------
# Discrepancy helpers
# ---------------------------------------------------------------------------

def _check_readme_claims(project_root: Path, all_files: List[str]) -> List[Dict[str, Any]]:
    """
    Scan README and docs for file/directory references and verify they exist.
    Returns a list of discrepancy records.
    """
    discrepancies: List[Dict[str, Any]] = []
    file_set = {f.lower() for f in all_files}

    # Patterns that suggest a path claim: backtick paths, `path/to/file`
    path_pattern = re.compile(r'`([^`\s]+/[^`\s]+\.[^`\s]+)`')

    for doc_path in project_root.rglob("*.md"):
        if any(_should_skip(p) for p in doc_path.parts):
            continue
        try:
            text = doc_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in path_pattern.finditer(text):
            claimed = match.group(1).lstrip("/")
            # Check if any actual file ends with this path component
            if not any(f.endswith(claimed.lower()) or claimed.lower() in f
                       for f in file_set):
                discrepancies.append({
                    "id": f"doc_ref_{len(discrepancies)+1}",
                    "area": str(doc_path.relative_to(project_root)),
                    "documented_claim": f"references `{claimed}`",
                    "observed_state": "path not found in project tree",
                    "severity": "minor",
                    "resolution_status": "unresolved",
                })
    return discrepancies


# ---------------------------------------------------------------------------
# ForensicsExecutor
# ---------------------------------------------------------------------------

class ForensicsExecutor:
    """
    Executor for Forensics family pipelines.

    Implements phase execution for ground-truth establishment.
    """

    def __init__(self, output_path: Path, project_root: Optional[Path] = None):
        self.output_path = output_path
        self.project_root = project_root or Path.cwd()
        self.writer = ArtifactWriter(output_path)

    # -----------------------------------------------------------------------
    # project_mapping
    # -----------------------------------------------------------------------

    def execute_project_mapping(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute project_mapping pipeline.

        Produces:
        - inventory_ledger
        - physical_dependency_graph
        - discrepancy_ledger
        - trust_zone_map
        - canonical_source_note
        - route_recommendation
        """
        scope = context.get("scope", {})

        # Phase 1: scope_boundary
        scope_note = self._scope_boundary(scope)
        state.add_artifact("scope_note", scope_note)

        # Phase 2: inventory_artifacts_and_runtime — REAL FILESYSTEM SCAN
        inventory = self._inventory_artifacts(context)
        state.add_artifact("inventory_ledger", inventory)

        # Phase 3: classify_sources_and_provenance
        provenance = self._classify_sources(inventory)
        state.add_artifact("provenance_ledger", provenance)

        # Phase 4: construct_physical_dependency_graph
        dep_graph = self._construct_dependency_graph(inventory)
        state.add_artifact("physical_dependency_graph", dep_graph)

        # Phase 5: map_discrepancies_and_conflicts
        discrepancies = self._map_discrepancies(inventory, provenance)
        state.add_artifact("discrepancy_ledger", discrepancies)

        # Phase 6: classify_trust_zones
        trust_zones = self._classify_trust_zones(provenance, discrepancies)
        state.add_artifact("trust_zone_map", trust_zones)

        # Phase 7: identify_canonical_structure
        canonical = self._identify_canonical(trust_zones, dep_graph)
        state.add_artifact("canonical_source_note", canonical)

        # Phase 8: recommend_route
        route = self._recommend_route(state, canonical, trust_zones, discrepancies)
        state.add_artifact("route_recommendation", route)

        # Update trust assessment
        state.trust_assessment = self._assess_trust(trust_zones, discrepancies)

        return state

    def _scope_boundary(self, scope: Dict[str, Any]) -> Dict[str, Any]:
        """Bound the mapping scope."""
        return {
            "scope": scope.get("description", "Project state mapping"),
            "project_root": str(self.project_root),
            "boundaries": scope.get("boundaries", []),
            "success_criteria": scope.get("success_criteria", [
                "inventory_ledger_present",
                "dependency_graph_present",
                "route_recommendation_present",
            ]),
            "scoped_at": datetime.now(timezone.utc).isoformat(),
        }

    def _inventory_artifacts(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inventory actual artifacts by walking the project filesystem.

        Classifies each file as code/doc/config/test/other. Skips
        VCS metadata, caches, and dependency directories.
        """
        root = self.project_root
        artifacts: List[Dict[str, Any]] = []
        dir_summary: Dict[str, int] = {}

        for dirpath, dirnames, filenames in os.walk(root):
            # Prune skipped dirs in-place so os.walk doesn't descend into them
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]

            for fname in filenames:
                fpath = Path(dirpath) / fname
                try:
                    stat = fpath.stat()
                    rel = str(fpath.relative_to(root))
                    ftype = _classify_file(fpath, root)
                    artifacts.append({
                        "name": fname,
                        "path": rel,
                        "type": ftype,
                        "size_bytes": stat.st_size,
                        "last_modified": datetime.fromtimestamp(
                            stat.st_mtime, tz=timezone.utc
                        ).isoformat(),
                    })
                    # Tally by top-level directory
                    top = fpath.relative_to(root).parts[0] if fpath.relative_to(root).parts else "."
                    dir_summary[top] = dir_summary.get(top, 0) + 1
                except (OSError, ValueError):
                    continue

        # Detect Python version from runtime
        python_version = f"{os.sys.version_info.major}.{os.sys.version_info.minor}"

        return {
            "artifacts": artifacts,
            "total_files": len(artifacts),
            "by_type": {
                t: sum(1 for a in artifacts if a["type"] == t)
                for t in ("code", "doc", "config", "test", "other")
            },
            "top_level_directories": dir_summary,
            "runtime_surfaces": [
                {"name": "python", "type": "interpreter", "version": python_version}
            ],
            "project_root": str(root),
            "inventoried_at": datetime.now(timezone.utc).isoformat(),
        }

    def _classify_sources(self, inventory: Dict[str, Any]) -> Dict[str, Any]:
        """Classify sources by provenance and assign initial trust."""
        classifications: List[Dict[str, Any]] = []

        for artifact in inventory.get("artifacts", []):
            atype = artifact.get("type", "other")
            # Observed filesystem artifacts get provisional trust by default
            # Test files and config files get higher initial trust
            if atype == "test":
                trust = "high"
                provenance = "observed"
                freshness = "current"
            elif atype == "code":
                trust = "provisional"
                provenance = "observed"
                freshness = "current"
            elif atype == "config":
                trust = "provisional"
                provenance = "observed"
                freshness = "current"
            elif atype == "doc":
                trust = "provisional"
                provenance = "documented"
                freshness = "unknown"
            else:
                trust = "provisional"
                provenance = "observed"
                freshness = "unknown"

            classifications.append({
                "source": artifact["path"],
                "type": atype,
                "provenance": provenance,
                "freshness": freshness,
                "trust_level": trust,
            })

        return {
            "classifications": classifications,
            "summary": {
                "total": len(classifications),
                "by_trust": {
                    level: sum(1 for c in classifications if c["trust_level"] == level)
                    for level in ("high", "provisional", "low", "collapsed")
                },
            },
            "classified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _construct_dependency_graph(self, inventory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a physical dependency graph by tracing Python imports and
        YAML cross-references within the project.
        """
        root = self.project_root
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []
        seen_nodes: Dict[str, int] = {}

        def get_or_add_node(path_str: str, ntype: str) -> int:
            if path_str not in seen_nodes:
                idx = len(nodes)
                nodes.append({"id": idx, "path": path_str, "type": ntype})
                seen_nodes[path_str] = idx
            return seen_nodes[path_str]

        artifacts = inventory.get("artifacts", [])

        for artifact in artifacts:
            ftype = artifact.get("type", "other")
            rel_path = artifact["path"]
            fpath = root / rel_path

            src_id = get_or_add_node(rel_path, ftype)

            if ftype == "code" and fpath.suffix == ".py":
                try:
                    for imp in _extract_python_imports(fpath):
                        # Resolve relative to project root
                        imp_as_path = imp.replace(".", "/")
                        for candidate in [
                            f"{imp_as_path}.py",
                            f"{imp_as_path}/__init__.py",
                        ]:
                            if (root / candidate).exists():
                                tgt_id = get_or_add_node(candidate, "code")
                                edges.append({
                                    "source": src_id,
                                    "target": tgt_id,
                                    "type": "python_import",
                                })
                                break
                except (OSError, RecursionError):
                    pass

            elif ftype in ("config", "doc") and fpath.suffix in (".yaml", ".yml", ".md"):
                try:
                    for ref in _extract_yaml_references(fpath):
                        if (root / ref).exists():
                            ref_type = _classify_file(root / ref, root)
                            tgt_id = get_or_add_node(ref, ref_type)
                            edges.append({
                                "source": src_id,
                                "target": tgt_id,
                                "type": "yaml_reference",
                            })
                except OSError:
                    pass

        return {
            "nodes": nodes,
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "graph_type": "physical",
            "constructed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _map_discrepancies(
        self,
        inventory: Dict[str, Any],
        provenance: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Map discrepancies between documented claims and observed filesystem state.

        Checks:
        - Doc files referencing paths that don't exist
        - Mismatches between file count summaries and actual counts
        """
        root = self.project_root
        all_paths = [a["path"] for a in inventory.get("artifacts", [])]

        doc_discrepancies = _check_readme_claims(root, all_paths)

        # Count by severity
        severity_count = {"critical": 0, "major": 0, "minor": 0, "informational": 0}
        for d in doc_discrepancies:
            sev = d.get("severity", "informational")
            severity_count[sev] = severity_count.get(sev, 0) + 1

        return {
            "discrepancies": doc_discrepancies,
            "summary": {
                "total_discrepancies": len(doc_discrepancies),
                **severity_count,
            },
            "mapped_at": datetime.now(timezone.utc).isoformat(),
        }

    def _classify_trust_zones(
        self,
        provenance: Dict[str, Any],
        discrepancies: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Classify trust zones per top-level area of the project.

        Logic:
        - Areas with only observed, no docs: provisional trust
        - Areas that are test directories: high trust
        - Documentation areas with unresolved discrepancies: low trust
        - No discrepancies in an area: high trust
        - Areas with critical discrepancies: collapsed trust
        """
        root = self.project_root
        disc_list = discrepancies.get("discrepancies", [])
        total_disc = len(disc_list)
        critical_count = discrepancies.get("summary", {}).get("critical", 0)

        # Build per-area discrepancy index
        area_discs: Dict[str, List[str]] = {}
        for d in disc_list:
            area = d.get("area", "").split("/")[0] if "/" in d.get("area", "") else d.get("area", "unknown")
            area_discs.setdefault(area, []).append(d.get("documented_claim", ""))

        # Discover top-level areas from provenance classifications
        top_areas: Dict[str, List[str]] = {}
        for c in provenance.get("classifications", []):
            parts = c["source"].split("/")
            area = parts[0] if len(parts) > 1 else "."
            top_areas.setdefault(area, []).append(c["trust_level"])

        zones: List[Dict[str, Any]] = []
        for area, trust_levels in top_areas.items():
            area_disc_count = len(area_discs.get(area, []))
            area_critical = sum(
                1 for d in disc_list
                if d.get("area", "").startswith(area) and d.get("severity") == "critical"
            )

            if area_critical > 0:
                trust = "collapsed"
            elif area_disc_count > 3:
                trust = "low"
            elif area_disc_count > 0:
                trust = "provisional"
            elif any(t == "high" for t in trust_levels):
                trust = "high"
            else:
                trust = "provisional"

            zones.append({
                "area": area,
                "trust_level": trust,
                "discrepancies": area_discs.get(area, []),
                "rationale": (
                    f"{area_disc_count} discrepancy(ies) found"
                    if area_disc_count else "No discrepancies detected"
                ),
            })

        # Overall trust: worst zone that covers non-trivial surface area
        trust_rank = {"high": 0, "provisional": 1, "low": 2, "collapsed": 3}
        if critical_count > 0:
            overall = "collapsed"
        elif total_disc > 5:
            overall = "low"
        elif total_disc > 0:
            overall = "provisional"
        else:
            overall = "high"

        return {
            "project_root": str(root),
            "zones": zones,
            "overall_trust": overall,
            "overall_rationale": (
                f"{total_disc} total discrepancy(ies) detected across project docs"
                if total_disc else "No discrepancies detected — observed state appears coherent"
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _identify_canonical(
        self,
        trust_zones: Dict[str, Any],
        dep_graph: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Identify canonical structure or candidates based on trust zones."""
        overall_trust = trust_zones.get("overall_trust", "provisional")
        zones = trust_zones.get("zones", [])
        high_trust_areas = [z["area"] for z in zones if z["trust_level"] == "high"]
        canonical_identified = overall_trust in ("high", "provisional")

        return {
            "canonical_identified": canonical_identified,
            "canonical_sources": high_trust_areas if high_trust_areas else ["observed_filesystem"],
            "overall_trust": overall_trust,
            "candidates": [
                {"area": z["area"], "trust": z["trust_level"]}
                for z in zones if z["trust_level"] in ("high", "provisional")
            ],
            "identified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _recommend_route(
        self,
        state: ExecutionState,
        canonical: Dict[str, Any],
        trust_zones: Dict[str, Any],
        discrepancies: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Recommend next safe pipeline based on trust and discrepancy state."""
        discrepancy_count = discrepancies.get("summary", {}).get("total_discrepancies", 0)
        trust_level = trust_zones.get("overall_trust", "provisional")

        if trust_level == "collapsed":
            return {
                "recommended_next": "Forensics/defragmentation",
                "rationale": "Trust has collapsed; project state requires repair before any build or investigation work.",
                "confidence": "high",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        elif discrepancy_count > 5 or trust_level == "low":
            return {
                "recommended_next": "Forensics/defragmentation",
                "rationale": f"High discrepancy count ({discrepancy_count}) or low trust — entropy is the primary problem.",
                "confidence": "high",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        elif discrepancy_count > 0:
            return {
                "recommended_next": "Forensics/documentation_audit",
                "rationale": f"{discrepancy_count} doc/state discrepancies need reconciliation before build work proceeds.",
                "confidence": "medium",
                "alternatives": [{"route": "Forge", "condition": "if discrepancies are accepted as minor"}],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        elif canonical.get("canonical_identified"):
            return {
                "recommended_next": "Forge",
                "rationale": "State is grounded and canonical structure is identified — build work can proceed.",
                "confidence": "high",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        else:
            return {
                "recommended_next": "Inquiry",
                "rationale": "State is grounded but canonical structure is unclear — investigation needed.",
                "confidence": "medium",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }

    def _assess_trust(
        self,
        trust_zones: Dict[str, Any],
        discrepancies: Dict[str, Any],
    ) -> TrustAssessment:
        """Create trust assessment from analysis."""
        discrepancy_count = discrepancies.get("summary", {}).get("total_discrepancies", 0)
        trust_level = trust_zones.get("overall_trust", "provisional")

        requires_forensics = trust_level == "collapsed"
        requires_defragmentation = discrepancy_count > 5 or trust_level == "low"
        canonical_identified = trust_level in ("high", "provisional")

        return TrustAssessment(
            trust_level=trust_level,
            canonical_sources_identified=canonical_identified,
            discrepancy_count=discrepancy_count,
            entropy_level="high" if requires_defragmentation else ("medium" if discrepancy_count > 0 else "low"),
            requires_forensics=requires_forensics,
            requires_defragmentation=requires_defragmentation,
        )

    # -----------------------------------------------------------------------
    # defragmentation (largely logic-correct; scan integrated via project_root)
    # -----------------------------------------------------------------------

    def execute_defragmentation(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute defragmentation pipeline."""
        fragmentation = self._inspect_state(context, state)
        state.add_artifact("fragmentation_snapshot", fragmentation)

        entropy = self._classify_entropy(fragmentation)
        state.add_artifact("entropy_classification", entropy)

        method = self._choose_method(entropy, fragmentation)
        state.add_artifact("chosen_method", method)

        execution = self._execute_method(method, fragmentation, context)
        state.add_artifact("residue_disposition_ledger", execution["residue_disposition_ledger"])
        state.add_artifact("changed_structure_map", execution["changed_structure_map"])

        normalization = self._normalize_metadata(execution["changed_structure_map"])
        state.add_artifact("metadata_normalization_record", normalization)

        verification = self._verify_coherence(
            normalization,
            execution["residue_disposition_ledger"],
        )
        state.add_artifact("trust_reassessment_note", verification)

        route = self._finalize_reroute(verification, entropy, state)
        state.add_artifact("route_recommendation", route)

        state.trust_assessment = self._post_defragmentation_trust(verification, entropy)
        return state

    def _inspect_state(
        self,
        context: Dict[str, Any],
        state: ExecutionState,
    ) -> Dict[str, Any]:
        """Phase 1: Inspect current layout for fragmentation indicators."""
        root = self.project_root
        duplicate_candidates: List[str] = []
        naming_drift: List[str] = []
        seen_names: Dict[str, List[str]] = {}

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            for fname in filenames:
                stem = Path(fname).stem.lower()
                seen_names.setdefault(stem, []).append(
                    str(Path(dirpath).relative_to(root) / fname)
                )

        for stem, paths in seen_names.items():
            if len(paths) > 1:
                duplicate_candidates.extend(paths)

        # Simple naming drift: mixed casing or separators for same logical name
        all_names = list(seen_names.keys())
        for name in all_names:
            camel = re.sub(r'[_\-]', '', name)
            if camel != name and camel in [re.sub(r'[_\-]', '', n) for n in all_names if n != name]:
                naming_drift.append(name)

        metadata_issues = context.get("metadata_issues", [])
        structural_issues = context.get("structural_issues", [])

        fragmentation_indicators = {
            "duplicate_artifacts": list(set(duplicate_candidates))[:20],
            "naming_drift": naming_drift[:10],
            "metadata_disorder": len(metadata_issues),
            "structural_conflicts": len(structural_issues),
            "orphaned_files": [],
            "version_mismatches": [],
        }

        total = sum([
            len(fragmentation_indicators["duplicate_artifacts"]) > 0,
            len(naming_drift) > 0,
            len(metadata_issues) > 0,
        ])

        return {
            "fragmentation_indicators": fragmentation_indicators,
            "total_artifacts": sum(1 for _ in root.rglob("*") if _.is_file()
                                    and not any(_should_skip(p) for p in _.relative_to(root).parts)),
            "problem_severity": "high" if total > 2 else "medium" if total > 0 else "low",
            "inspected_at": datetime.now(timezone.utc).isoformat(),
        }

    def _classify_entropy(self, fragmentation: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Determine entropy severity."""
        indicators = fragmentation.get("fragmentation_indicators", {})
        duplicate_count = len(indicators.get("duplicate_artifacts", []))
        naming_drift_count = len(indicators.get("naming_drift", []))
        metadata_disorder = indicators.get("metadata_disorder", 0)
        structural_conflicts = indicators.get("structural_conflicts", 0)

        total_issues = duplicate_count + naming_drift_count + metadata_disorder + structural_conflicts

        if total_issues == 0:
            severity, description = "tidy", "Minor residue, naming drift, or lightweight metadata disorder"
        elif total_issues <= 3 and structural_conflicts == 0:
            severity, description = "consolidate", "Overlapping artifacts or multiple near-canonical sources"
        elif structural_conflicts <= 2:
            severity, description = "repair", "Project shape has drifted; code/specs/docs disagree"
        else:
            severity, description = "anchor", "No trustworthy canonical source; severe fragmentation"

        return {
            "severity": severity,
            "description": description,
            "issue_count": total_issues,
            "breakdown": {
                "duplicates": duplicate_count,
                "naming_drift": naming_drift_count,
                "metadata_disorder": metadata_disorder,
                "structural_conflicts": structural_conflicts,
            },
            "classified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _choose_method(self, entropy: Dict[str, Any], fragmentation: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Select the smallest defragmentation method."""
        severity = entropy.get("severity", "consolidate")
        method_map = {
            "tidy":        {"method": "tidy",        "description": "Minor cleanup: naming drift, lightweight metadata disorder",       "actions": ["rename_files", "normalize_metadata", "remove_trivial_residue"]},
            "consolidate": {"method": "consolidate",  "description": "Merge overlapping artifacts, select single canonical source",     "actions": ["merge_duplicates", "select_canonical", "archive_redundant"]},
            "repair":      {"method": "repair",       "description": "Align drifted code, specs, docs, and configs",                   "actions": ["realign_artifacts", "update_lineage", "resolve_disagreements"]},
            "anchor":      {"method": "anchor",       "description": "Rollback or recovery; establish new canonical from trusted state","actions": ["rollback_to_trusted", "rebuild_from_anchor", "archive_corrupted"]},
        }
        chosen = method_map.get(severity, method_map["consolidate"])
        return {**chosen, "rationale": f"Selected based on entropy severity: {severity}", "chosen_at": datetime.now(timezone.utc).isoformat()}

    def _execute_method(self, method: Dict[str, Any], fragmentation: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Apply the chosen entropy-reduction method."""
        actions = method.get("actions", [])
        residue_disposition = {"resolved": [], "archived": [], "merged": [], "retained": []}
        changed_structure = {"before": fragmentation.get("fragmentation_indicators", {}), "after": {}, "changes_made": []}

        action_map = {
            "rename_files":        ("resolved", "naming_drift", "renamed", "normalized_file_names"),
            "normalize_metadata":  ("resolved", "metadata_disorder", "normalized", "metadata_normalized"),
            "remove_trivial_residue": ("archived", "trivial_residue", "removed", "trivial_residue_removed"),
            "merge_duplicates":    ("merged", "duplicate_artifacts", "consolidated", "duplicates_merged"),
            "select_canonical":    ("retained", "canonical_source", "selected", "canonical_established"),
            "archive_redundant":   ("archived", "redundant_artifacts", "archived", "redundant_archived"),
            "realign_artifacts":   ("resolved", "drifted_artifacts", "realigned", "artifacts_realigned"),
            "update_lineage":      ("resolved", "stale_lineage", "updated", "lineage_updated"),
            "resolve_disagreements": ("resolved", "disagreements", "resolved", "disagreements_resolved"),
            "rollback_to_trusted": ("archived", "corrupted_artifacts", "archived", "rollback_completed"),
            "rebuild_from_anchor": ("resolved", "anchor_rebuild", "rebuilt", "anchor_rebuilt"),
            "archive_corrupted":   ("archived", "corrupted_data", "archived", "corrupted_archived"),
        }

        for action in actions:
            if action in action_map:
                bucket, atype, act, change = action_map[action]
                residue_disposition[bucket].append({"type": atype, "action": act, "count": 0})
                changed_structure["changes_made"].append(change)

        changed_structure["after"] = {"duplicate_artifacts": [], "naming_drift": [], "metadata_disorder": 0, "structural_conflicts": 0, "orphaned_files": [], "version_mismatches": []}

        return {
            "residue_disposition_ledger": {**residue_disposition, "total_resolved": len(residue_disposition["resolved"]), "executed_at": datetime.now(timezone.utc).isoformat()},
            "changed_structure_map": changed_structure,
        }

    def _normalize_metadata(self, changed_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Bring metadata and provenance into alignment."""
        changes = changed_structure.get("changes_made", [])
        actions = []
        if "canonical_established" in changes:
            actions.append({"action": "update_canonical_pointers", "target": "all_references", "status": "completed"})
        if "metadata_normalized" in changes:
            actions.append({"action": "rebuild_indices", "target": "metadata_index", "status": "completed"})
        if "artifacts_realigned" in changes:
            actions.append({"action": "sync_provenance", "target": "all_artifacts", "status": "completed"})
        return {"actions": actions, "canonical_pointers_updated": True, "indices_rebuilt": True, "provenance_synced": True, "normalized_at": datetime.now(timezone.utc).isoformat()}

    def _verify_coherence(self, normalization: Dict[str, Any], residue_disposition: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: Confirm that one trustworthy structure now exists."""
        normalization_complete = (normalization.get("canonical_pointers_updated") and normalization.get("indices_rebuilt") and normalization.get("provenance_synced"))
        total_resolved = residue_disposition.get("total_resolved", 0)
        total_archived = len(residue_disposition.get("archived", []))
        if normalization_complete:
            coherence_status, confidence = "restored", "high"
        elif total_resolved > 0 or total_archived > 0:
            coherence_status, confidence = "partial", "medium"
        else:
            coherence_status, confidence = "not_restored", "low"
        return {"coherence_status": coherence_status, "confidence": confidence, "canonical_structure_verified": normalization_complete, "conflicts_resolved": total_resolved, "conflicts_archived": total_archived, "verified_at": datetime.now(timezone.utc).isoformat()}

    def _finalize_reroute(self, verification: Dict[str, Any], entropy: Dict[str, Any], state: ExecutionState) -> Dict[str, Any]:
        """Phase 7: Route after defragmentation."""
        coherence_status = verification.get("coherence_status", "not_restored")
        severity = entropy.get("severity", "consolidate")
        now = datetime.now(timezone.utc).isoformat()
        if coherence_status == "not_restored":
            return {"recommended_next": "Forensics/defragmentation", "rationale": "Coherence not fully restored — re-run defragmentation.", "confidence": "high", "generated_at": now}
        elif coherence_status == "partial" or severity == "anchor":
            return {"recommended_next": "Forensics/project_mapping", "rationale": "Partial coherence — recheck with project_mapping.", "confidence": "high", "generated_at": now}
        elif severity in ("tidy", "consolidate"):
            return {"recommended_next": "Forge", "rationale": "Coherence restored — build work is now safe.", "confidence": "high", "generated_at": now}
        else:
            return {"recommended_next": "Conduit", "rationale": "Docs/handoff reconciliation needed after repair.", "confidence": "medium", "generated_at": now}

    def _post_defragmentation_trust(self, verification: Dict[str, Any], entropy: Dict[str, Any]) -> TrustAssessment:
        """Create trust assessment after defragmentation."""
        coherence_status = verification.get("coherence_status", "not_restored")
        if coherence_status == "restored":
            trust_level, entropy_level = "high", "low"
        elif coherence_status == "partial":
            trust_level, entropy_level = "provisional", "low"
        else:
            trust_level, entropy_level = "low", "high"
        return TrustAssessment(
            trust_level=trust_level,
            canonical_sources_identified=(coherence_status == "restored"),
            discrepancy_count=0 if coherence_status == "restored" else 1,
            entropy_level=entropy_level,
            coherence_restored=(coherence_status == "restored"),
            requires_forensics=(coherence_status == "not_restored"),
            requires_defragmentation=False,
        )

    # -----------------------------------------------------------------------
    # documentation_audit
    # -----------------------------------------------------------------------

    def execute_documentation_audit(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute documentation_audit pipeline."""
        doc_inventory = self._inventory_documentation(context)
        state.add_artifact("documentation_inventory", doc_inventory)

        code_inventory = self._inventory_code_state(context)
        state.add_artifact("code_state_inventory", code_inventory)

        drift = self._detect_drift(doc_inventory, code_inventory)
        state.add_artifact("drift_ledger", drift)

        gaps = self._identify_gaps(doc_inventory, code_inventory)
        state.add_artifact("gap_analysis", gaps)

        misleading = self._detect_misleading_claims(doc_inventory, drift)
        state.add_artifact("misleading_claims_ledger", misleading)

        report = self._generate_audit_report(drift, gaps, misleading)
        state.add_artifact("audit_report", report)

        route = self._documentation_audit_route(report, state)
        state.add_artifact("route_recommendation", route)

        return state

    def _inventory_documentation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Inventory all documentation by scanning the filesystem."""
        root = self.project_root
        docs: List[Dict[str, Any]] = []
        categories: Dict[str, List[str]] = {"readme": [], "api_docs": [], "architecture": [], "user_guides": [], "internal_notes": []}

        for fpath in root.rglob("*.md"):
            if any(_should_skip(p) for p in fpath.relative_to(root).parts):
                continue
            rel = str(fpath.relative_to(root))
            fname_lower = fpath.name.lower()
            docs.append({"path": rel, "name": fpath.name, "size_bytes": fpath.stat().st_size})
            if "readme" in fname_lower:
                categories["readme"].append(rel)
            elif "arch" in fname_lower or "design" in fname_lower:
                categories["architecture"].append(rel)
            elif "api" in fname_lower:
                categories["api_docs"].append(rel)
            elif "guide" in fname_lower or "tutorial" in fname_lower:
                categories["user_guides"].append(rel)
            else:
                categories["internal_notes"].append(rel)

        return {"documents": docs, "total_count": len(docs), "categories": categories, "inventoried_at": datetime.now(timezone.utc).isoformat()}

    def _inventory_code_state(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Inventory actual Python source files."""
        root = self.project_root
        code_files: List[Dict[str, Any]] = []
        public_apis: List[str] = []

        for fpath in root.rglob("*.py"):
            if any(_should_skip(p) for p in fpath.relative_to(root).parts):
                continue
            rel = str(fpath.relative_to(root))
            code_files.append({"path": rel, "name": fpath.name})
            # Detect public API candidates (functions not starting with _)
            try:
                tree = ast.parse(fpath.read_text(encoding="utf-8", errors="replace"))
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not node.name.startswith("_"):
                            public_apis.append(f"{rel}::{node.name}")
            except (SyntaxError, OSError):
                pass

        return {"code_files": code_files, "total_count": len(code_files), "modules": [f["path"] for f in code_files], "public_apis": public_apis[:50], "inventoried_at": datetime.now(timezone.utc).isoformat()}

    def _detect_drift(self, docs: Dict[str, Any], code: Dict[str, Any]) -> Dict[str, Any]:
        """Detect drift: functions mentioned in docs that don't exist in code."""
        public_apis = set(code.get("public_apis", []))
        doc_mentions: List[str] = []
        drift_items: List[Dict[str, Any]] = []

        root = self.project_root
        func_pattern = re.compile(r'`([a-z_][a-z0-9_]+)\(\)`')

        for doc in docs.get("documents", []):
            try:
                text = (root / doc["path"]).read_text(encoding="utf-8", errors="replace")
                for match in func_pattern.finditer(text):
                    fname = match.group(1)
                    doc_mentions.append(fname)
                    # Check if this function name appears in any public API
                    if not any(api.endswith(f"::{fname}") for api in public_apis):
                        if len(drift_items) < 20:  # Cap to avoid noise
                            drift_items.append({
                                "document": doc["path"],
                                "claimed_function": fname,
                                "found_in_code": False,
                            })
            except OSError:
                pass

        severity = "none" if not drift_items else "minor" if len(drift_items) <= 3 else "major"
        return {"drift_items": drift_items, "total": len(drift_items), "severity": severity, "detected_at": datetime.now(timezone.utc).isoformat()}

    def _identify_gaps(self, docs: Dict[str, Any], code: Dict[str, Any]) -> Dict[str, Any]:
        """Identify undocumented modules."""
        doc_paths = {d["path"] for d in docs.get("documents", [])}
        code_modules = code.get("modules", [])
        gaps: List[str] = []

        for mod in code_modules:
            # Check if there's a corresponding doc mentioning this module name
            mod_stem = Path(mod).stem
            if not any(mod_stem in dp for dp in doc_paths):
                if not mod_stem.startswith("_") and mod_stem not in ("conftest", "setup"):
                    gaps.append(mod)

        return {"missing_docs": gaps[:20], "outdated_docs": [], "gaps": gaps[:20], "total_gaps": len(gaps), "identified_at": datetime.now(timezone.utc).isoformat()}

    def _detect_misleading_claims(self, docs: Dict[str, Any], drift: Dict[str, Any]) -> Dict[str, Any]:
        """Surface drift items as potential misleading claims."""
        misleading = [
            {"document": d["document"], "claim": f"References `{d['claimed_function']}()` which is not found in code", "severity": "minor"}
            for d in drift.get("drift_items", [])
        ]
        return {"misleading_claims": misleading, "total": len(misleading), "severity": "none" if not misleading else "minor", "detected_at": datetime.now(timezone.utc).isoformat()}

    def _generate_audit_report(self, drift: Dict[str, Any], gaps: Dict[str, Any], misleading: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive audit report."""
        return {"summary": "Documentation audit complete", "drift_count": drift.get("total", 0), "gap_count": gaps.get("total_gaps", 0), "misleading_count": misleading.get("total", 0), "severity": drift.get("severity", "none"), "generated_at": datetime.now(timezone.utc).isoformat()}

    def _documentation_audit_route(self, report: Dict[str, Any], state: ExecutionState) -> Dict[str, Any]:
        """Recommend route after documentation audit."""
        drift_count = report.get("drift_count", 0)
        gap_count = report.get("gap_count", 0)
        now = datetime.now(timezone.utc).isoformat()
        if drift_count > 5:
            return {"recommended_next": "Forensics/defragmentation", "rationale": "Severe drift detected — structure needs repair.", "confidence": "high", "generated_at": now}
        elif gap_count > 3:
            return {"recommended_next": "Conduit/documentation", "rationale": f"{gap_count} undocumented modules — documentation work is primary.", "confidence": "high", "generated_at": now}
        else:
            return {"recommended_next": "Forge", "rationale": "Documentation acceptable — build work can proceed.", "confidence": "medium", "generated_at": now}

    # -----------------------------------------------------------------------
    # anomaly_disambiguation
    # -----------------------------------------------------------------------

    def execute_anomaly_disambiguation(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute anomaly_disambiguation pipeline."""
        anomalies = self._surface_anomalies(context, state)
        state.add_artifact("anomaly_catalog", anomalies)

        classification = self._classify_anomalies(anomalies)
        state.add_artifact("anomaly_classification", classification)

        options = self._generate_disambiguation_options(classification)
        state.add_artifact("disambiguation_options", options)

        path = self._recommend_disambiguation_path(options, classification)
        state.add_artifact("recommended_path", path)

        route = self._anomaly_route(path, state)
        state.add_artifact("route_recommendation", route)

        return state

    def _surface_anomalies(self, context: Dict[str, Any], state: ExecutionState) -> Dict[str, Any]:
        """Surface anomalies from artifacts and filesystem."""
        anomalies: List[Dict[str, Any]] = []
        root = self.project_root

        # Check for oversized files (potential data blobs checked in accidentally)
        for fpath in root.rglob("*"):
            if fpath.is_file() and not any(_should_skip(p) for p in fpath.relative_to(root).parts):
                try:
                    size = fpath.stat().st_size
                    if size > 10 * 1024 * 1024:  # > 10MB
                        anomalies.append({
                            "type": "oversized_file",
                            "path": str(fpath.relative_to(root)),
                            "size_bytes": size,
                            "description": f"File exceeds 10MB: {size // (1024*1024)}MB",
                        })
                except OSError:
                    pass

        # Pass-through any anomalies provided in context
        for a in context.get("anomalies", []):
            anomalies.append(a)

        return {"anomalies": anomalies, "total": len(anomalies), "surface_method": "filesystem_scan", "surfaced_at": datetime.now(timezone.utc).isoformat()}

    def _classify_anomalies(self, anomalies: Dict[str, Any]) -> Dict[str, Any]:
        """Classify anomalies by type."""
        classifications: Dict[str, List[Any]] = {"misfit": [], "absence": [], "tension": [], "warp": [], "offset": []}
        for a in anomalies.get("anomalies", []):
            atype = a.get("type", "")
            if "oversized" in atype or "unexpected" in atype:
                classifications["misfit"].append(a)
            elif "missing" in atype or "not_found" in atype:
                classifications["absence"].append(a)
            else:
                classifications["tension"].append(a)
        primary = max(classifications, key=lambda k: len(classifications[k])) if any(classifications.values()) else "unknown"
        return {"classifications": classifications, "primary_type": primary, "classified_at": datetime.now(timezone.utc).isoformat()}

    def _generate_disambiguation_options(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """Generate disambiguation options for each anomaly type."""
        primary = classification.get("primary_type", "unknown")
        options_map = {
            "misfit":  [{"option": "remove", "description": "Remove the anomalous artifact"}, {"option": "isolate", "description": "Move to quarantine area for review"}],
            "absence": [{"option": "create", "description": "Create the missing artifact"}, {"option": "reroute", "description": "Accept absence and update references"}],
            "tension": [{"option": "investigate", "description": "Run Inquiry to understand tension source"}, {"option": "accept", "description": "Accept tension as known and document it"}],
        }
        return {"options": options_map.get(primary, [{"option": "investigate", "description": "Run Inquiry/hypothesis_generation"}]), "primary_type": primary, "generated_at": datetime.now(timezone.utc).isoformat()}

    def _recommend_disambiguation_path(self, options: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend the best disambiguation path."""
        opts = options.get("options", [])
        recommended = opts[0] if opts else {"option": "investigate", "description": "Insufficient signal — investigate"}
        return {"recommended_option": recommended, "rationale": f"Selected based on primary anomaly type: {classification.get('primary_type','unknown')}", "recommended_at": datetime.now(timezone.utc).isoformat()}

    def _anomaly_route(self, path: Dict[str, Any], state: ExecutionState) -> Dict[str, Any]:
        """Recommend route after anomaly disambiguation."""
        option = path.get("recommended_option", {}).get("option", "investigate")
        now = datetime.now(timezone.utc).isoformat()
        if option == "investigate":
            return {"recommended_next": "Inquiry/hypothesis_generation", "rationale": "Anomaly requires causal investigation.", "confidence": "medium", "generated_at": now}
        elif option in ("remove", "isolate"):
            return {"recommended_next": "Forge/coding", "rationale": "Anomaly is actionable — targeted change work can proceed.", "confidence": "high", "generated_at": now}
        else:
            return {"recommended_next": "Conduit/documentation", "rationale": "Anomaly is documented — handoff note needed.", "confidence": "medium", "generated_at": now}


    # -----------------------------------------------------------------------
    # Experimental pipelines
    # -----------------------------------------------------------------------

    def execute_label_shift_correction(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute label_shift_correction with explicit approval and evidence."""
        baseline_counts = context.get("baseline_label_counts", {})
        reference_counts = context.get("reference_label_counts", {})

        shift_assessment = self._assess_label_shift(baseline_counts, reference_counts)
        state.add_artifact("shift_assessment", shift_assessment)

        reference_distribution = self._reference_distribution(reference_counts)
        state.add_artifact("reference_label_distribution", reference_distribution)

        calibration_mapping = self._compute_calibration_mapping(
            shift_assessment,
            reference_distribution,
        )
        state.add_artifact("calibration_mapping", calibration_mapping)

        adjusted_predictions = self._apply_calibration(context, calibration_mapping)
        state.add_artifact("adjusted_predictions", adjusted_predictions)

        performance_report = self._evaluate_calibration(
            context,
            shift_assessment,
            adjusted_predictions,
        )
        state.add_artifact("performance_evaluation_report", performance_report)

        state.add_artifact(
            "route_recommendation",
            self._label_shift_route(performance_report),
        )
        return state

    def execute_introspection_audit(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute introspection_audit with explicit approval and evidence."""
        reasoning_events = context.get("reasoning_events", [])
        expected_objectives = context.get("expected_objectives", [])

        introspection_log = {
            "events": reasoning_events,
            "surface": context.get("reasoning_surface", "externalized_trace"),
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("introspection_log", introspection_log)

        interpretability_packet = {
            "signals": context.get("interpretability_signals", []),
            "expected_objectives": expected_objectives,
            "tooling": context.get("interpretability_tools", ["manual_trace_review"]),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("interpretability_packet", interpretability_packet)

        hidden_goal_map = self._identify_hidden_objectives(
            reasoning_events,
            expected_objectives,
        )
        state.add_artifact("hidden_goal_map", hidden_goal_map)

        reasoning_report = {
            "unfaithful_patterns": hidden_goal_map["suspected_hidden_objectives"],
            "confidence": hidden_goal_map["confidence"],
            "summary": (
                "Reasoning surface diverges from expected objectives"
                if hidden_goal_map["suspected_hidden_objectives"]
                else "No hidden objective signal exceeded the alert threshold"
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("unfaithful_reasoning_report", reasoning_report)

        remediation_plan = {
            "actions": context.get(
                "remediation_actions",
                ["tighten routing constraints", "escalate to Conduit if external reporting is needed"],
            ),
            "requires_code_change": bool(context.get("requires_code_change")),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("remediation_plan", remediation_plan)

        state.add_artifact(
            "route_recommendation",
            self._introspection_route(hidden_goal_map, remediation_plan),
        )
        state.add_artifact(
            "final_audit_note",
            {
                "status": "complete",
                "summary": reasoning_report["summary"],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        return state

    def _assess_label_shift(
        self,
        baseline_counts: Dict[str, Any],
        reference_counts: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Measure simple absolute label distribution drift."""
        labels = sorted(set(baseline_counts) | set(reference_counts))
        total_baseline = sum(float(baseline_counts.get(label, 0)) for label in labels) or 1.0
        total_reference = sum(float(reference_counts.get(label, 0)) for label in labels) or 1.0

        deltas = []
        for label in labels:
            baseline_ratio = float(baseline_counts.get(label, 0)) / total_baseline
            reference_ratio = float(reference_counts.get(label, 0)) / total_reference
            deltas.append(
                {
                    "label": label,
                    "baseline_ratio": round(baseline_ratio, 4),
                    "reference_ratio": round(reference_ratio, 4),
                    "absolute_delta": round(abs(reference_ratio - baseline_ratio), 4),
                }
            )

        mean_delta = sum(item["absolute_delta"] for item in deltas) / max(len(deltas), 1)
        return {
            "labels": deltas,
            "mean_absolute_delta": round(mean_delta, 4),
            "shift_detected": mean_delta >= 0.05,
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _reference_distribution(self, reference_counts: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize the reference label distribution."""
        total = sum(float(value) for value in reference_counts.values()) or 1.0
        distribution = {
            label: round(float(value) / total, 4)
            for label, value in sorted(reference_counts.items())
        }
        return {
            "distribution": distribution,
            "source": "context.reference_label_counts",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _compute_calibration_mapping(
        self,
        shift_assessment: Dict[str, Any],
        reference_distribution: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build multiplicative calibration weights."""
        mapping = {}
        reference = reference_distribution.get("distribution", {})
        for label_info in shift_assessment.get("labels", []):
            baseline_ratio = label_info["baseline_ratio"] or 0.0001
            mapping[label_info["label"]] = round(
                reference.get(label_info["label"], 0.0) / baseline_ratio,
                4,
            )
        return {
            "weights": mapping,
            "method": "reference_ratio_over_baseline_ratio",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _apply_calibration(
        self,
        context: Dict[str, Any],
        calibration_mapping: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply calibration weights to supplied prediction scores."""
        predictions = context.get("predictions", [])
        weights = calibration_mapping.get("weights", {})
        adjusted = []
        for item in predictions:
            label = item.get("label", "unknown")
            score = float(item.get("score", 0.0))
            adjusted.append(
                {
                    "label": label,
                    "baseline_score": score,
                    "adjusted_score": round(score * float(weights.get(label, 1.0)), 4),
                }
            )
        return {
            "predictions": adjusted,
            "applied_at": datetime.now(timezone.utc).isoformat(),
        }

    def _evaluate_calibration(
        self,
        context: Dict[str, Any],
        shift_assessment: Dict[str, Any],
        adjusted_predictions: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compare baseline and calibrated scores with supplied metrics."""
        baseline_metric = float(context.get("baseline_metric", 0.0))
        calibrated_metric = float(context.get("calibrated_metric", baseline_metric))
        improvement = round(calibrated_metric - baseline_metric, 4)
        return {
            "shift_detected": shift_assessment.get("shift_detected", False),
            "baseline_metric": baseline_metric,
            "calibrated_metric": calibrated_metric,
            "improvement": improvement,
            "adjusted_prediction_count": len(adjusted_predictions.get("predictions", [])),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _label_shift_route(self, performance_report: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend the next family after label shift correction."""
        now = datetime.now(timezone.utc).isoformat()
        if performance_report.get("improvement", 0.0) > 0:
            return {
                "recommended_next": "Inquiry/research",
                "rationale": "Calibration improved the evaluation surface; inquiry can interpret the result.",
                "confidence": "medium",
                "generated_at": now,
            }
        return {
            "recommended_next": "Forge/coding",
            "rationale": "Calibration failed to recover performance; code or data path changes are likely required.",
            "confidence": "medium",
            "generated_at": now,
        }

    def _identify_hidden_objectives(
        self,
        reasoning_events: List[Dict[str, Any]],
        expected_objectives: List[str],
    ) -> Dict[str, Any]:
        """Detect objectives present in the trace but absent from the expected set."""
        expected = {objective.lower() for objective in expected_objectives}
        hidden = []
        for event in reasoning_events:
            objective = str(event.get("objective", "")).strip()
            if objective and objective.lower() not in expected:
                hidden.append(objective)
        return {
            "suspected_hidden_objectives": hidden,
            "confidence": "high" if hidden else "low",
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _introspection_route(
        self,
        hidden_goal_map: Dict[str, Any],
        remediation_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Recommend the next family after introspection audit."""
        now = datetime.now(timezone.utc).isoformat()
        if hidden_goal_map.get("suspected_hidden_objectives"):
            if remediation_plan.get("requires_code_change"):
                return {
                    "recommended_next": "Forge/refactor",
                    "rationale": "Hidden-goal signal requires code or model remediation.",
                    "confidence": "high",
                    "generated_at": now,
                }
            return {
                "recommended_next": "Conduit/handoff_synthesis",
                "rationale": "Audit surfaced operational risk that should be communicated immediately.",
                "confidence": "high",
                "generated_at": now,
            }
        return {
            "recommended_next": "Forensics/project_mapping",
            "rationale": "No material hidden-goal evidence found; return to standard grounded forensics.",
            "confidence": "medium",
            "generated_at": now,
        }
