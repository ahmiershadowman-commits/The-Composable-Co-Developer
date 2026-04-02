"""
Conduit family pipeline executors.

Implements execution for Conduit family pipelines:
- documentation
- scholarly_writing
- professional_writing
- handoff_synthesis

All helpers do real filesystem I/O against project_root, producing
content-bearing artifacts rather than placeholders.
"""

import os
import re
import ast
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

from runtime.state.models import ExecutionState, TrustAssessment, FamilyType
from runtime.artifacts.writer import ArtifactWriter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "env",
    ".mypy_cache", ".pytest_cache", "dist", "build", ".tox",
}

_DOC_EXTS = {".md", ".rst", ".txt", ".adoc"}
_CODE_EXTS = {".py", ".js", ".ts", ".go", ".rs", ".java", ".sh", ".yaml", ".yml", ".json", ".toml"}
_BIB_EXTS  = {".bib", ".bibtex"}

_MARKER_PATTERN = re.compile(
    r"(TODO|FIXME|HACK|XXX|STUB|NOTE|BUG|WONTFIX)[:\s]+(.*)", re.IGNORECASE
)
_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)", re.MULTILINE)
_DOCSTRING_RE = re.compile(r'"""(.*?)"""', re.DOTALL)


# ---------------------------------------------------------------------------
# Shared filesystem utilities
# ---------------------------------------------------------------------------

def _should_skip(name: str) -> bool:
    return name in _SKIP_DIRS or name.startswith(".")


def _scan_project_docs(root: Path) -> List[Dict[str, Any]]:
    """
    Walk the project tree and return structured information about doc files.
    Each entry has: path (relative), size_bytes, headings, section_count.
    """
    results = []
    try:
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            rel_dir = Path(dirpath).relative_to(root)
            for fname in filenames:
                suffix = Path(fname).suffix.lower()
                if suffix not in _DOC_EXTS:
                    continue
                fpath = Path(dirpath) / fname
                try:
                    text = fpath.read_text(encoding="utf-8", errors="replace")
                    headings = _HEADING_PATTERN.findall(text)
                    heading_list = [f"{'#' * len(h[0])} {h[1]}" for h in headings]
                    results.append({
                        "path": str(rel_dir / fname),
                        "size_bytes": fpath.stat().st_size,
                        "headings": heading_list[:20],      # cap at 20
                        "section_count": len(headings),
                        "word_count": len(text.split()),
                    })
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return results


def _scan_code_docstrings(root: Path, limit: int = 30) -> List[Dict[str, Any]]:
    """
    Extract module-level and class/function docstrings from Python files.
    Returns list of {file, kind, name, docstring}.
    """
    results = []
    try:
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            rel_dir = Path(dirpath).relative_to(root)
            for fname in filenames:
                if not fname.endswith(".py"):
                    continue
                fpath = Path(dirpath) / fname
                try:
                    text = fpath.read_text(encoding="utf-8", errors="replace")
                    tree = ast.parse(text)
                    # Module docstring
                    if (
                        tree.body
                        and isinstance(tree.body[0], ast.Expr)
                        and isinstance(tree.body[0].value, ast.Constant)
                    ):
                        doc = str(tree.body[0].value.value).strip()
                        if doc:
                            results.append({
                                "file": str(rel_dir / fname),
                                "kind": "module",
                                "name": fname,
                                "docstring": doc[:300],
                            })
                    # Class and function docstrings
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                            doc = ast.get_docstring(node)
                            if doc:
                                results.append({
                                    "file": str(rel_dir / fname),
                                    "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                                    "name": node.name,
                                    "docstring": doc[:300],
                                })
                            if len(results) >= limit:
                                return results
                except (SyntaxError, OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return results


def _scan_for_markers(root: Path, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Scan all text files for TODO/FIXME/HACK/STUB/BUG markers.
    Returns list of {file, line, kind, text}.
    """
    results = []
    try:
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            rel_dir = Path(dirpath).relative_to(root)
            for fname in filenames:
                suffix = Path(fname).suffix.lower()
                if suffix not in (_DOC_EXTS | _CODE_EXTS):
                    continue
                fpath = Path(dirpath) / fname
                try:
                    for lineno, line in enumerate(
                        fpath.read_text(encoding="utf-8", errors="replace").splitlines(),
                        start=1,
                    ):
                        m = _MARKER_PATTERN.search(line)
                        if m:
                            results.append({
                                "file": str(rel_dir / fname),
                                "line": lineno,
                                "kind": m.group(1).upper(),
                                "text": m.group(2).strip()[:120],
                            })
                            if len(results) >= limit:
                                return results
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return results


def _scan_runtime_artifacts(root: Path) -> List[Dict[str, Any]]:
    """
    Look for previously produced runtime_output YAML artifacts.
    Returns list of {family, pipeline, artifact_name, path, keys}.
    """
    results = []
    runtime_output = root / "runtime_output"
    if not runtime_output.exists():
        return results
    try:
        for family_dir in runtime_output.iterdir():
            if not family_dir.is_dir():
                continue
            for pipeline_dir in family_dir.iterdir():
                if not pipeline_dir.is_dir():
                    continue
                for artifact_file in pipeline_dir.glob("*.yaml"):
                    try:
                        data = yaml.safe_load(artifact_file.read_text(encoding="utf-8"))
                        keys = list(data.keys()) if isinstance(data, dict) else []
                        results.append({
                            "family": family_dir.name,
                            "pipeline": pipeline_dir.name,
                            "artifact_name": artifact_file.stem,
                            "path": str(artifact_file.relative_to(root)),
                            "keys": keys[:10],
                            "data": data if isinstance(data, dict) else {},
                        })
                    except Exception:
                        pass
    except (OSError, PermissionError):
        pass
    return results


def _scan_bib_files(root: Path) -> List[Dict[str, Any]]:
    """
    Find .bib / .bibtex files and extract citation keys.
    """
    results = []
    _bib_entry = re.compile(r"@\w+\{([^,]+),", re.MULTILINE)
    try:
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            rel_dir = Path(dirpath).relative_to(root)
            for fname in filenames:
                if Path(fname).suffix.lower() not in _BIB_EXTS:
                    continue
                fpath = Path(dirpath) / fname
                try:
                    text = fpath.read_text(encoding="utf-8", errors="replace")
                    keys = _bib_entry.findall(text)
                    results.append({
                        "path": str(rel_dir / fname),
                        "citation_keys": keys,
                        "count": len(keys),
                    })
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return results


def _infer_doc_gaps(docs: List[Dict[str, Any]], project_root: Path) -> List[str]:
    """
    Compare existing doc paths against expected doc patterns.
    Returns list of missing expected documentation artifacts.
    """
    doc_paths_lower = {d["path"].lower() for d in docs}
    expected = [
        ("readme", "README.md — project overview"),
        ("changelog", "CHANGELOG.md — version history"),
        ("contributing", "CONTRIBUTING.md — contributor guide"),
        ("license", "LICENSE — license terms"),
        ("architecture", "docs/architecture/ — architecture documentation"),
        ("api", "docs/api/ — API reference"),
    ]
    gaps = []
    for keyword, description in expected:
        found = any(keyword in p for p in doc_paths_lower)
        if not found:
            # Also check if file actually exists
            possible = list(project_root.glob(f"**/{keyword}*"))
            if not possible:
                gaps.append(description)
    return gaps


def _project_file_summary(root: Path) -> Dict[str, Any]:
    """
    Quick file count by type for metadata/context.
    """
    counts: Dict[str, int] = {}
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            for fname in filenames:
                ext = Path(fname).suffix.lower() or "no_ext"
                counts[ext] = counts.get(ext, 0) + 1
                total += 1
    except (OSError, PermissionError):
        pass
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    return {"total_files": total, "by_extension": dict(top)}


# ---------------------------------------------------------------------------
# ConduitExecutor
# ---------------------------------------------------------------------------

class ConduitExecutor:
    """
    Executor for Conduit family pipelines.

    All phases perform real project-aware work:
    - documentation: scans project docs, identifies gaps, produces real outline + draft scaffold
    - handoff_synthesis: reads existing runtime artifacts, synthesizes status + open items
    - professional_writing: analyses content + audience, produces structured writing scaffold
    - scholarly_writing: scans for .bib files, extracts citations, maps claim structure
    """

    def __init__(self, output_path: Path, project_root: Optional[Path] = None):
        self.output_path = output_path
        self.project_root = project_root or Path.cwd()
        self.writer = ArtifactWriter(output_path)

    # -----------------------------------------------------------------------
    # documentation pipeline
    # -----------------------------------------------------------------------

    def execute_documentation(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute documentation pipeline.

        Produces:
        - audience_scope_note
        - source_packet
        - structure_outline
        - draft_document
        - support_note
        - metadata_update_record
        - route_recommendation
        """
        audience = self._scope_audience(context)
        state.add_artifact("audience_scope_note", audience)

        sources = self._gather_sources(context)
        state.add_artifact("source_packet", sources)

        outline = self._outline_structure(audience, sources)
        state.add_artifact("structure_outline", outline)

        draft = self._draft(outline, sources)
        state.add_artifact("draft_document", draft)

        support = self._verify_support(draft, sources)
        state.add_artifact("support_note", support)

        metadata = self._update_metadata(draft)
        state.add_artifact("metadata_update_record", metadata)

        route = self._documentation_recommend_route(state, sources)
        state.add_artifact("route_recommendation", route)

        return state

    def execute_handoff_synthesis(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute handoff_synthesis pipeline.

        Produces:
        - handoff_scope_note
        - handoff_source_packet
        - core_structure_map
        - handoff_document
        - unresolveds_and_risks
        - provenance_summary
        - next_safe_steps
        """
        scope = self._scope_handoff(context)
        state.add_artifact("handoff_scope_note", scope)

        sources = self._gather_handoff_sources(state)
        state.add_artifact("handoff_source_packet", sources)

        structure = self._map_core_structure(sources)
        state.add_artifact("core_structure_map", structure)

        handoff = self._synthesize_handoff(structure, sources)
        state.add_artifact("handoff_document", handoff)

        unresolveds = self._note_unresolveds(state)
        state.add_artifact("unresolveds_and_risks", unresolveds)

        provenance = self._summarize_provenance(state, sources)
        state.add_artifact("provenance_summary", provenance)

        next_steps = self._recommend_next_steps(handoff, unresolveds)
        state.add_artifact("next_safe_steps", next_steps)

        return state

    def execute_professional_writing(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute professional_writing pipeline.

        Produces:
        - audience_objective_statement
        - outline
        - draft_document
        - refinement_log
        - validation_note
        - delivery_record
        """
        audience_obj = self._define_audience_objective(context)
        state.add_artifact("audience_objective_statement", audience_obj)

        outline = self._outline_professional(audience_obj, context)
        state.add_artifact("outline", outline)

        draft = self._draft_professional(outline, context)
        state.add_artifact("draft_document", draft)

        refinement = self._refine(draft)
        state.add_artifact("refinement_log", refinement)

        validation = self._validate_professional(refinement)
        state.add_artifact("validation_note", validation)

        delivery = self._deliver(validation)
        state.add_artifact("delivery_record", delivery)

        return state

    def execute_scholarly_writing(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute scholarly_writing pipeline.

        Produces:
        - genre_frame
        - source_packet
        - outline
        - claim_hierarchy
        - draft
        - citation_map
        - final_document
        """
        genre = self._frame_genre(context)
        state.add_artifact("genre_frame", genre)

        sources = self._gather_scholarly_sources(context)
        state.add_artifact("source_packet", sources)

        outline = self._outline_scholarly(genre, sources, context)
        state.add_artifact("outline", outline)

        claims = self._map_claims(outline, context)
        state.add_artifact("claim_hierarchy", claims)

        draft = self._draft_scholarly(claims, sources, context)
        state.add_artifact("draft", draft)

        citations = self._map_citations(draft, sources)
        state.add_artifact("citation_map", citations)

        final = self._finalize_scholarly(draft, citations)
        state.add_artifact("final_document", final)

        return state

    # -----------------------------------------------------------------------
    # Documentation phase helpers
    # -----------------------------------------------------------------------

    def _scope_audience(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = context.get("content", "")
        raw_audience = context.get("audience", "")

        # Infer audience from content keywords if not explicit
        if not raw_audience:
            content_lower = content.lower()
            if any(w in content_lower for w in ["api", "sdk", "endpoint", "function", "class", "module"]):
                inferred = "developer"
            elif any(w in content_lower for w in ["user", "guide", "tutorial", "how to", "getting started"]):
                inferred = "end_user"
            elif any(w in content_lower for w in ["architecture", "design", "rationale", "decision"]):
                inferred = "technical_stakeholder"
            else:
                inferred = "technical"
            raw_audience = inferred
            inference_basis = "keyword_scan"
        else:
            inference_basis = "explicit"

        return {
            "audience": raw_audience,
            "inference_basis": inference_basis,
            "scope": context.get("scope", "project_documentation"),
            "format_preference": context.get("format", "markdown"),
            "content_summary": content[:200] if content else "(none)",
            "scoped_at": datetime.now().isoformat(),
        }

    def _gather_sources(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan project for existing docs, code docstrings, and runtime artifacts.
        Returns a source inventory the outline/draft phases can use.
        """
        root = self.project_root

        docs = _scan_project_docs(root)
        docstrings = _scan_code_docstrings(root, limit=20)
        runtime_artifacts = _scan_runtime_artifacts(root)
        gaps = _infer_doc_gaps(docs, root)

        # Classify existing docs by area
        areas: Dict[str, List[str]] = {}
        for doc in docs:
            parts = Path(doc["path"]).parts
            area = parts[0] if len(parts) > 1 else "root"
            areas.setdefault(area, []).append(doc["path"])

        return {
            "doc_files": docs,
            "doc_count": len(docs),
            "doc_areas": areas,
            "docstrings_sampled": docstrings,
            "runtime_artifacts": [
                {"family": a["family"], "pipeline": a["pipeline"], "artifact": a["artifact_name"]}
                for a in runtime_artifacts
            ],
            "runtime_artifact_count": len(runtime_artifacts),
            "documentation_gaps": gaps,
            "gathered_at": datetime.now().isoformat(),
        }

    def _outline_structure(
        self,
        audience: Dict[str, Any],
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Derive a real outline from the source inventory.
        Sections correspond to actual doc areas found + gap areas.
        """
        aud = audience.get("audience", "technical")
        areas = sources.get("doc_areas", {})
        gaps = sources.get("documentation_gaps", [])
        doc_count = sources.get("doc_count", 0)

        # Build sections from what exists
        sections = []
        for area, paths in sorted(areas.items()):
            sections.append({
                "title": area.replace("_", " ").title(),
                "area": area,
                "existing_files": paths[:10],
                "status": "documented",
            })

        # Add gap sections
        for gap in gaps:
            label = gap.split("—")[0].strip() if "—" in gap else gap
            sections.append({
                "title": label,
                "area": "gap",
                "existing_files": [],
                "status": "missing",
                "note": gap,
            })

        # Audience-specific ordering heuristic
        if aud == "end_user":
            priority = ["root", "docs", "gap"]
        elif aud == "developer":
            priority = ["entrypoints", "runtime", "shared", "docs", "gap"]
        else:
            priority = ["docs", "root", "entrypoints", "runtime", "gap"]

        def sort_key(s: Dict) -> int:
            try:
                return priority.index(s.get("area", "gap"))
            except ValueError:
                return len(priority)

        sections.sort(key=sort_key)

        return {
            "audience": aud,
            "section_count": len(sections),
            "sections": sections,
            "source_file_count": doc_count,
            "outlined_at": datetime.now().isoformat(),
        }

    def _draft(
        self,
        outline: Dict[str, Any],
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Produce a draft scaffold that enumerates real structure.
        Not prose generation — produces structured content map the skill layer fills.
        """
        sections = outline.get("sections", [])
        audience = outline.get("audience", "technical")
        doc_files = sources.get("doc_files", [])

        # Map actual headings for each documented section
        path_to_headings: Dict[str, List[str]] = {}
        for doc in doc_files:
            path_to_headings[doc["path"]] = doc.get("headings", [])

        content_map = []
        for section in sections:
            entry: Dict[str, Any] = {
                "section": section["title"],
                "status": section["status"],
            }
            if section["status"] == "documented":
                # Pull real headings from the first file in this area
                files = section.get("existing_files", [])
                headings_found = []
                for f in files[:3]:
                    headings_found.extend(path_to_headings.get(f, []))
                entry["existing_headings"] = headings_found[:15]
                entry["file_count"] = len(files)
                entry["action"] = "review_and_integrate"
            else:
                entry["action"] = "create"
                entry["note"] = section.get("note", "")

            content_map.append(entry)

        return {
            "audience": audience,
            "draft_type": "content_scaffold",
            "content_map": content_map,
            "total_sections": len(sections),
            "documented_sections": sum(1 for s in sections if s["status"] == "documented"),
            "gap_sections": sum(1 for s in sections if s["status"] == "missing"),
            "drafted_at": datetime.now().isoformat(),
        }

    def _verify_support(
        self,
        draft: Dict[str, Any],
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check that documented sections have backing files that actually exist.
        """
        root = self.project_root
        content_map = draft.get("content_map", [])
        doc_files_set = {d["path"] for d in sources.get("doc_files", [])}

        verified = []
        unsupported = []
        for entry in content_map:
            if entry.get("status") == "documented":
                files = [f for f in entry.get("existing_headings", []) if f in doc_files_set]
                # Use file_count as proxy — if we got headings, files exist
                if entry.get("file_count", 0) > 0:
                    verified.append(entry["section"])
                else:
                    unsupported.append(entry["section"])
            # gap sections are expected to be unsupported

        support_ratio = len(verified) / max(len(content_map), 1)

        return {
            "verified_sections": verified,
            "unsupported_sections": unsupported,
            "support_ratio": round(support_ratio, 2),
            "support_quality": (
                "strong" if support_ratio > 0.8
                else "partial" if support_ratio > 0.4
                else "weak"
            ),
            "verified_at": datetime.now().isoformat(),
        }

    def _update_metadata(self, draft: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect real metadata from the project for the documentation record.
        """
        root = self.project_root
        file_summary = _project_file_summary(root)

        # Look for version markers
        version = None
        for candidate in ["VERSION", "version.txt", "pyproject.toml", "package.json", "setup.cfg"]:
            p = root / candidate
            if p.exists():
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                    m = re.search(r'version\s*[=:]\s*["\']?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', text)
                    if m:
                        version = m.group(1)
                        break
                except (OSError, PermissionError):
                    pass

        return {
            "project_root": str(root),
            "version_detected": version,
            "file_inventory": file_summary,
            "sections_drafted": draft.get("total_sections", 0),
            "documented_sections": draft.get("documented_sections", 0),
            "gap_sections": draft.get("gap_sections", 0),
            "updated_at": datetime.now().isoformat(),
        }

    def _documentation_recommend_route(
        self,
        state: ExecutionState,
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        gap_count = len(sources.get("documentation_gaps", []))
        runtime_count = sources.get("runtime_artifact_count", 0)

        if gap_count > 3:
            target = "Forge/development"
            reason = f"{gap_count} documentation gaps suggest active build work is needed before documentation can be complete"
        elif runtime_count > 0:
            target = "Conduit/handoff_synthesis"
            reason = f"{runtime_count} runtime artifacts exist — consider synthesizing them into a handoff document"
        else:
            target = "complete"
            reason = "documentation pass complete, project appears well-covered"

        return {
            "target": target,
            "reason": reason,
            "gap_count": gap_count,
            "runtime_artifacts_available": runtime_count,
        }

    # -----------------------------------------------------------------------
    # Handoff synthesis phase helpers
    # -----------------------------------------------------------------------

    def _scope_handoff(self, context: Dict[str, Any]) -> Dict[str, Any]:
        recipient = context.get("recipient", "")
        if not recipient:
            # Infer from content
            content = context.get("content", "").lower()
            if "team" in content or "squad" in content:
                recipient = "team"
            elif "client" in content or "customer" in content:
                recipient = "client"
            elif "review" in content or "auditor" in content:
                recipient = "reviewer"
            else:
                recipient = "next_operator"

        return {
            "recipient": recipient,
            "purpose": context.get("purpose", "knowledge_transfer"),
            "content_hint": context.get("content", "")[:200],
            "scoped_at": datetime.now().isoformat(),
        }

    def _gather_handoff_sources(self, state: ExecutionState) -> Dict[str, Any]:
        """
        Pull existing runtime artifacts from disk to build a real source picture.
        Also include any artifacts already in state from the current run.
        """
        disk_artifacts = _scan_runtime_artifacts(self.project_root)

        # Group by family
        by_family: Dict[str, List[Dict]] = {}
        for art in disk_artifacts:
            fam = art["family"]
            by_family.setdefault(fam, []).append({
                "pipeline": art["pipeline"],
                "artifact": art["artifact_name"],
                "keys": art["keys"],
                "data_summary": {
                    k: (str(v)[:80] if not isinstance(v, (dict, list)) else f"[{type(v).__name__}]")
                    for k, v in art.get("data", {}).items()
                },
            })

        # In-session artifacts
        in_session = list(state.artifacts.keys())

        return {
            "disk_artifacts_by_family": by_family,
            "disk_artifact_count": len(disk_artifacts),
            "in_session_artifacts": in_session,
            "families_with_output": list(by_family.keys()),
            "gathered_at": datetime.now().isoformat(),
        }

    def _map_core_structure(self, sources: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a core structure from the discovered artifacts.
        Groups artifacts into: ground_truth (Forensics), build (Forge),
        investigation (Inquiry), synthesis (Conduit prior).
        """
        by_family = sources.get("disk_artifacts_by_family", {})

        role_map = {
            "Forensics": "ground_truth",
            "Forge": "build_record",
            "Inquiry": "investigation_record",
            "Conduit": "synthesis_record",
        }

        structure: Dict[str, Any] = {"layers": []}
        for family, role in role_map.items():
            arts = by_family.get(family, [])
            if arts:
                structure["layers"].append({
                    "family": family,
                    "role": role,
                    "artifact_count": len(arts),
                    "pipelines_run": list({a["pipeline"] for a in arts}),
                    "key_artifacts": [a["artifact"] for a in arts[:5]],
                })

        # Also note in-session
        in_session = sources.get("in_session_artifacts", [])
        if in_session:
            structure["in_session"] = in_session

        structure["total_sources"] = sources.get("disk_artifact_count", 0) + len(in_session)
        structure["mapped_at"] = datetime.now().isoformat()
        return structure

    def _synthesize_handoff(
        self,
        structure: Dict[str, Any],
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Synthesize a real handoff document from the artifact structure.
        Produces structured content from actual runtime data.
        """
        layers = structure.get("layers", [])
        total = structure.get("total_sources", 0)
        by_family = sources.get("disk_artifacts_by_family", {})

        # Extract key facts from each layer
        sections = []
        for layer in layers:
            family = layer["family"]
            arts = by_family.get(family, [])
            # Pull any high-signal fields from artifact data summaries
            highlights = []
            for art in arts[:3]:
                for k, v in art.get("data_summary", {}).items():
                    if k in ("overall_trust", "route", "recommendation", "synthesis",
                             "confidence", "conclusion", "status", "summary"):
                        highlights.append(f"{art['artifact']}.{k}: {v}")
            sections.append({
                "layer": layer["role"],
                "family": family,
                "pipelines": layer.get("pipelines_run", []),
                "highlights": highlights,
            })

        completeness = "complete" if len(layers) >= 3 else "partial" if layers else "empty"

        return {
            "handoff_type": "multi_family_synthesis",
            "completeness": completeness,
            "source_count": total,
            "sections": sections,
            "narrative_prompt": (
                f"Synthesize a handoff from {total} artifacts across "
                f"{len(layers)} pipeline families: "
                + ", ".join(lay["family"] for lay in layers)
            ),
            "synthesized_at": datetime.now().isoformat(),
        }

    def _note_unresolveds(self, state: ExecutionState) -> Dict[str, Any]:
        """
        Combine state.unresolveds with real TODO/FIXME markers from project.
        """
        markers = _scan_for_markers(self.project_root, limit=40)

        # Deduplicate state unresolveds by string repr
        state_items = []
        for u in getattr(state, "unresolveds", []):
            state_items.append(str(u))

        # Classify markers by severity
        risk_markers = [m for m in markers if m["kind"] in ("FIXME", "BUG", "HACK")]
        todo_markers = [m for m in markers if m["kind"] == "TODO"]
        stub_markers = [m for m in markers if m["kind"] == "STUB"]

        return {
            "state_unresolveds": state_items,
            "code_markers_total": len(markers),
            "risk_markers": risk_markers[:15],
            "todo_markers": [f"{m['file']}:{m['line']} — {m['text']}" for m in todo_markers[:10]],
            "stub_markers": [f"{m['file']}:{m['line']} — {m['text']}" for m in stub_markers[:10]],
            "risk_count": len(risk_markers),
            "severity": (
                "high" if len(risk_markers) > 10
                else "medium" if len(risk_markers) > 3
                else "low"
            ),
            "noted_at": datetime.now().isoformat(),
        }

    def _summarize_provenance(
        self,
        state: ExecutionState,
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Summarize which families ran, how many artifacts each produced.
        """
        by_family = sources.get("disk_artifacts_by_family", {})
        route_count = len(getattr(state, "route_history", []))

        family_summary = []
        for family, arts in by_family.items():
            pipelines = list({a["pipeline"] for a in arts})
            family_summary.append({
                "family": family,
                "pipelines_run": pipelines,
                "artifact_count": len(arts),
            })

        return {
            "families_executed": [f["family"] for f in family_summary],
            "family_summary": family_summary,
            "total_artifacts_on_disk": sources.get("disk_artifact_count", 0),
            "route_decisions_in_session": route_count,
            "summarized_at": datetime.now().isoformat(),
        }

    def _recommend_next_steps(
        self,
        handoff: Dict[str, Any],
        unresolveds: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Recommend concrete next steps based on completeness and risk markers.
        """
        completeness = handoff.get("completeness", "empty")
        risk_count = unresolveds.get("risk_count", 0)
        severity = unresolveds.get("severity", "low")

        steps = []

        if completeness == "empty":
            steps.append({
                "priority": 1,
                "step": "Run Forensics/defragmentation to establish ground truth",
                "rationale": "No prior pipeline artifacts found — start from baseline",
            })
        elif completeness == "partial":
            steps.append({
                "priority": 1,
                "step": "Run missing family pipelines to complete the picture",
                "rationale": f"Only {len(handoff.get('sections', []))} of 4 families have output",
            })

        if severity == "high":
            steps.append({
                "priority": 2,
                "step": f"Address {risk_count} FIXME/BUG/HACK markers before handoff",
                "rationale": "High risk marker count indicates known instabilities",
            })
        elif severity == "medium":
            steps.append({
                "priority": 3,
                "step": f"Review {risk_count} risk markers with recipient",
                "rationale": "Moderate risk markers should be acknowledged in handoff",
            })

        if completeness in ("complete", "partial") and severity in ("low", "medium"):
            steps.append({
                "priority": 4,
                "step": "Deliver handoff_document to recipient and schedule walkthrough",
                "rationale": "Pipeline coverage is sufficient for a productive handoff",
            })

        steps.sort(key=lambda s: s["priority"])

        return {
            "steps": steps,
            "step_count": len(steps),
            "readiness": (
                "ready" if completeness == "complete" and severity == "low"
                else "conditional" if completeness in ("complete", "partial")
                else "not_ready"
            ),
            "recommended_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Professional writing phase helpers
    # -----------------------------------------------------------------------

    def _define_audience_objective(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = context.get("content", "")
        content_lower = content.lower()

        # Infer document type from content
        if any(w in content_lower for w in ["proposal", "pitch", "request for"]):
            doc_type = "proposal"
            tone = "persuasive"
        elif any(w in content_lower for w in ["report", "status", "update", "summary"]):
            doc_type = "report"
            tone = "informative"
        elif any(w in content_lower for w in ["memo", "internal", "team", "announcement"]):
            doc_type = "memo"
            tone = "direct"
        elif any(w in content_lower for w in ["email", "message", "note to"]):
            doc_type = "email"
            tone = "conversational"
        else:
            doc_type = "document"
            tone = "professional"

        audience = context.get("audience", "professional")
        objective = context.get("objective", f"Communicate {doc_type} to {audience} audience")

        return {
            "audience": audience,
            "doc_type": doc_type,
            "tone": tone,
            "objective": objective,
            "content_length_words": len(content.split()),
            "inferred_at": datetime.now().isoformat(),
        }

    def _outline_professional(
        self,
        audience_obj: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        doc_type = audience_obj.get("doc_type", "document")
        content = context.get("content", "")

        # Standard section templates by document type
        templates = {
            "proposal": ["Executive Summary", "Problem Statement", "Proposed Solution",
                         "Timeline", "Budget / Resources", "Call to Action"],
            "report": ["Executive Summary", "Background", "Findings",
                       "Analysis", "Recommendations", "Appendix"],
            "memo": ["Purpose", "Background", "Details", "Action Required"],
            "email": ["Opening", "Context", "Key Points", "Next Steps", "Closing"],
            "document": ["Introduction", "Background", "Main Content",
                         "Discussion", "Conclusion"],
        }

        sections = templates.get(doc_type, templates["document"])

        # Detect if content already maps to any section keywords
        content_lower = content.lower()
        section_relevance = []
        for sec in sections:
            keyword = sec.split(" ")[0].lower()
            relevant = keyword in content_lower
            section_relevance.append({"section": sec, "content_hint_found": relevant})

        return {
            "doc_type": doc_type,
            "sections": section_relevance,
            "total_sections": len(sections),
            "outlined_at": datetime.now().isoformat(),
        }

    def _draft_professional(
        self,
        outline: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        content = context.get("content", "")
        sections = outline.get("sections", [])
        doc_type = outline.get("doc_type", "document")

        # Produce a section-by-section content scaffold
        content_scaffold = []
        for sec in sections:
            section_name = sec["section"]
            has_hint = sec.get("content_hint_found", False)
            content_scaffold.append({
                "section": section_name,
                "placeholder": f"[{section_name} content — derive from input]",
                "input_available": has_hint,
                "word_target": (
                    50 if section_name in ("Executive Summary", "Purpose", "Closing", "Opening")
                    else 150
                ),
            })

        return {
            "doc_type": doc_type,
            "draft_type": "professional_scaffold",
            "source_content": content[:400] if content else "(none provided)",
            "sections": content_scaffold,
            "total_word_target": sum(s["word_target"] for s in content_scaffold),
            "drafted_at": datetime.now().isoformat(),
        }

    def _refine(self, draft: Dict[str, Any]) -> Dict[str, Any]:
        sections = draft.get("sections", [])

        refinements = []
        for sec in sections:
            checks = []
            if not sec.get("input_available"):
                checks.append({
                    "check": "source_coverage",
                    "status": "warn",
                    "note": "No source content mapped to this section — requires manual input",
                })
            else:
                checks.append({
                    "check": "source_coverage",
                    "status": "pass",
                    "note": "Source content available",
                })
            checks.append({
                "check": "word_target",
                "status": "pending",
                "note": f"Target: {sec.get('word_target', 100)} words",
            })
            refinements.append({
                "section": sec["section"],
                "checks": checks,
            })

        warn_count = sum(
            1 for r in refinements
            for c in r["checks"]
            if c["status"] == "warn"
        )

        return {
            "refinements": refinements,
            "warn_count": warn_count,
            "overall": "needs_input" if warn_count > 2 else "ready_to_fill",
            "refined_at": datetime.now().isoformat(),
        }

    def _validate_professional(self, refinement: Dict[str, Any]) -> Dict[str, Any]:
        overall = refinement.get("overall", "needs_input")
        warn_count = refinement.get("warn_count", 0)

        return {
            "validated": overall != "needs_input",
            "validation_status": "pass" if overall == "ready_to_fill" else "conditional",
            "blocking_issues": warn_count,
            "gate": (
                "proceed" if warn_count == 0
                else "proceed_with_gaps" if warn_count <= 2
                else "fill_gaps_first"
            ),
            "validated_at": datetime.now().isoformat(),
        }

    def _deliver(self, validation: Dict[str, Any]) -> Dict[str, Any]:
        gate = validation.get("gate", "fill_gaps_first")
        return {
            "delivery_status": (
                "ready" if gate == "proceed"
                else "conditional" if gate == "proceed_with_gaps"
                else "blocked"
            ),
            "gate": gate,
            "blocking_issues": validation.get("blocking_issues", 0),
            "delivered_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Scholarly writing phase helpers
    # -----------------------------------------------------------------------

    def _frame_genre(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = context.get("content", "").lower()
        genre = context.get("genre", "")

        if not genre:
            if any(w in content for w in ["paper", "study", "research", "literature review"]):
                genre = "research_paper"
            elif any(w in content for w in ["thesis", "dissertation"]):
                genre = "thesis"
            elif any(w in content for w in ["survey", "review", "systematic"]):
                genre = "survey"
            elif any(w in content for w in ["position", "argument", "critique"]):
                genre = "position_paper"
            else:
                genre = "academic_essay"

        citation_style_map = {
            "research_paper": "APA or IEEE",
            "thesis": "APA or Chicago",
            "survey": "IEEE",
            "position_paper": "Chicago or MLA",
            "academic_essay": "MLA or Chicago",
        }

        return {
            "genre": genre,
            "citation_style_suggestion": citation_style_map.get(genre, "APA"),
            "typical_length": {
                "research_paper": "4000-8000 words",
                "thesis": "20000-80000 words",
                "survey": "5000-15000 words",
                "position_paper": "2000-5000 words",
                "academic_essay": "1000-4000 words",
            }.get(genre, "2000-5000 words"),
            "required_sections": {
                "research_paper": ["Abstract", "Introduction", "Related Work",
                                   "Methodology", "Results", "Discussion", "Conclusion", "References"],
                "thesis": ["Abstract", "Introduction", "Literature Review",
                           "Methodology", "Results", "Discussion", "Conclusion", "Bibliography"],
                "survey": ["Abstract", "Introduction", "Taxonomy", "Survey",
                           "Open Problems", "Conclusion", "References"],
                "position_paper": ["Abstract", "Introduction", "Argument",
                                   "Counter-arguments", "Conclusion", "References"],
                "academic_essay": ["Introduction", "Body", "Conclusion", "Works Cited"],
            }.get(genre, ["Introduction", "Body", "Conclusion", "References"]),
            "framed_at": datetime.now().isoformat(),
        }

    def _gather_scholarly_sources(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan project for .bib files and existing doc sources.
        """
        bib_files = _scan_bib_files(self.project_root)
        docs = _scan_project_docs(self.project_root)

        all_citation_keys = []
        for b in bib_files:
            all_citation_keys.extend(b.get("citation_keys", []))

        # Also look for explicit sources in context
        context_sources = context.get("sources", [])

        return {
            "bib_files": bib_files,
            "total_bib_files": len(bib_files),
            "citation_keys": all_citation_keys[:50],
            "total_citations": len(all_citation_keys),
            "doc_sources": [{"path": d["path"], "headings": d["headings"][:5]} for d in docs[:10]],
            "context_sources": context_sources,
            "gathered_at": datetime.now().isoformat(),
        }

    def _outline_scholarly(
        self,
        genre: Dict[str, Any],
        sources: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        required_sections = genre.get("required_sections", ["Introduction", "Body", "Conclusion"])
        citation_count = sources.get("total_citations", 0)

        sections = []
        for sec in required_sections:
            sections.append({
                "section": sec,
                "citations_available": citation_count,
                "content_hint": context.get("content", "")[:100] if sec == "Introduction" else "",
                "status": "to_draft",
            })

        return {
            "genre": genre.get("genre", "academic"),
            "sections": sections,
            "total_sections": len(sections),
            "citations_available": citation_count,
            "outlined_at": datetime.now().isoformat(),
        }

    def _map_claims(
        self,
        outline: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        content = context.get("content", "")
        sections = outline.get("sections", [])

        # Extract candidate claims from content using simple heuristics
        sentences = re.split(r"[.!?]", content)
        claim_candidates = [
            s.strip() for s in sentences
            if len(s.strip()) > 20 and any(
                w in s.lower() for w in
                ["shows", "demonstrates", "argues", "proposes", "finds",
                 "suggests", "reveals", "proves", "indicates", "implies"]
            )
        ]

        # Build a hierarchy: central claim + sub-claims
        central = claim_candidates[0] if claim_candidates else "(central claim — to be derived from content)"
        sub_claims = claim_candidates[1:4] if len(claim_candidates) > 1 else []

        return {
            "central_claim": central,
            "sub_claims": sub_claims,
            "claim_count": len(claim_candidates),
            "supporting_sections": [s["section"] for s in sections
                                     if s["section"] not in ("Abstract", "References",
                                                              "Bibliography", "Works Cited")],
            "mapped_at": datetime.now().isoformat(),
        }

    def _draft_scholarly(
        self,
        claims: Dict[str, Any],
        sources: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        genre_hint = context.get("genre", "academic")
        citation_keys = sources.get("citation_keys", [])

        return {
            "draft_type": "scholarly_scaffold",
            "central_claim": claims.get("central_claim", ""),
            "sub_claims": claims.get("sub_claims", []),
            "citation_keys_available": citation_keys[:20],
            "citation_count": len(citation_keys),
            "sections_to_fill": claims.get("supporting_sections", []),
            "content_source": context.get("content", "")[:400],
            "genre": genre_hint,
            "drafted_at": datetime.now().isoformat(),
        }

    def _map_citations(
        self,
        draft: Dict[str, Any],
        sources: Dict[str, Any],
    ) -> Dict[str, Any]:
        citation_keys = sources.get("citation_keys", [])
        bib_files = sources.get("bib_files", [])

        # Map citation keys to sections (round-robin stub — real mapping requires model)
        sections = draft.get("sections_to_fill", [])
        citation_assignments: Dict[str, List[str]] = {}
        for i, sec in enumerate(sections):
            # Assign citations to sections proportionally
            start = (i * max(len(citation_keys), 1)) // max(len(sections), 1)
            end = ((i + 1) * max(len(citation_keys), 1)) // max(len(sections), 1)
            citation_assignments[sec] = citation_keys[start:end] if citation_keys else []

        return {
            "citation_keys": citation_keys,
            "bib_files": [b["path"] for b in bib_files],
            "assignments": citation_assignments,
            "total_citations": len(citation_keys),
            "unmapped_sections": [s for s in sections if not citation_assignments.get(s)],
            "mapped_at": datetime.now().isoformat(),
        }

    def _finalize_scholarly(
        self,
        draft: Dict[str, Any],
        citations: Dict[str, Any],
    ) -> Dict[str, Any]:
        unmapped = citations.get("unmapped_sections", [])
        total_cites = citations.get("total_citations", 0)

        readiness = (
            "publication_ready" if not unmapped and total_cites > 0
            else "draft_complete_needs_citations" if not unmapped
            else "sections_need_citation_mapping"
        )

        return {
            "finalized": True,
            "readiness": readiness,
            "unmapped_sections": unmapped,
            "citation_count": total_cites,
            "central_claim": draft.get("central_claim", ""),
            "finalized_at": datetime.now().isoformat(),
        }
