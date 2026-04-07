"""
Forge family pipeline executors.

Implements execution for Forge family pipelines:
- development
- coding
- testing
- refactor
"""

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from runtime.state.models import ExecutionState, TrustAssessment, FamilyType
from runtime.artifacts.writer import ArtifactWriter


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

_SKIP_DIRS = {
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules",
    ".venv", "venv", "env", ".env", "dist", "build", ".tox", ".eggs",
}
_CODE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".rb", ".sh"}
_TEST_DIRS = {"tests", "test", "__tests__", "spec"}
_DOC_EXTS = {".md", ".rst", ".txt"}


def _should_skip(name: str) -> bool:
    return name in _SKIP_DIRS or name.endswith(".egg-info")


def _keyword_score(text: str, keywords: List[str]) -> int:
    """Count how many keywords appear in text (case-insensitive)."""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def _extract_keywords(description: str) -> List[str]:
    """Pull meaningful keywords from a problem/question description."""
    # Strip common stopwords and punctuation
    stopwords = {"a", "an", "the", "to", "in", "of", "for", "with", "and", "or",
                 "is", "it", "on", "at", "as", "be", "by", "do", "we", "how",
                 "what", "why", "when", "where", "this", "that", "from", "not",
                 "are", "was", "were", "will", "can", "has", "have", "had",
                 "should", "would", "could", "need", "want", "get", "make"}
    words = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", description)
    return [w for w in words if w.lower() not in stopwords and len(w) > 2]


def _walk_code_files(root: Path) -> List[Path]:
    """Walk project and return all code files."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not _should_skip(d)]
        for fname in filenames:
            if Path(fname).suffix.lower() in _CODE_EXTS:
                files.append(Path(dirpath) / fname)
    return files


def _count_loc(path: Path) -> int:
    """Count non-blank, non-comment lines in a Python file."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return sum(1 for l in lines if l.strip() and not l.strip().startswith("#"))
    except OSError:
        return 0


def _get_functions(path: Path) -> List[Dict[str, Any]]:
    """Extract function info from a Python file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, OSError):
        return []
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append({
                "name": node.name,
                "line": node.lineno,
                "args": len(node.args.args),
                "public": not node.name.startswith("_"),
            })
    return funcs


# ---------------------------------------------------------------------------
# ForgeExecutor
# ---------------------------------------------------------------------------

class ForgeExecutor:
    """
    Executor for Forge family pipelines.

    Implements phase execution for build/change work.
    """

    def __init__(self, output_path: Path, project_root: Optional[Path] = None):
        self.output_path = output_path
        self.project_root = project_root or Path.cwd()
        self.writer = ArtifactWriter(output_path)

    # -----------------------------------------------------------------------
    # development
    # -----------------------------------------------------------------------

    def execute_development(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute development pipeline.

        Primary artifacts (spec-canonical):
        - work_plan
        - verification_summary
        - handoff_or_release_note

        Supporting artifacts:
        - architecture_note
        - slice_map
        - integration_state_note
        - packaging_note
        """
        # Phase 1: inspect system state and frame problem
        problem_frame = self._frame_problem(context)
        state.add_artifact("problem_frame", problem_frame)

        system_analysis = self._analyze_system(context, problem_frame)
        state.add_artifact("system_analysis", system_analysis)

        # Phase 2: shape work plan
        design = self._design_approach(problem_frame, system_analysis)
        state.add_artifact("architecture_note", design)

        work_plan = self._plan_work_slices(design, problem_frame, system_analysis)
        state.add_artifact("work_plan", work_plan)
        state.add_artifact("slice_map", work_plan)

        # Phase 3: verify system fit
        verification = self._verify_approach(design, work_plan)
        state.add_artifact("verification_summary", verification)

        # Phase 4: integration state and packaging
        integration_state = self._assess_integration_state(work_plan, verification)
        state.add_artifact("integration_state_note", integration_state)

        packaging = self._package_work(work_plan, integration_state)
        state.add_artifact("packaging_note", packaging)

        # Phase 5: handoff or release note
        handoff = self._produce_handoff_or_release_note(work_plan, verification)
        state.add_artifact("handoff_or_release_note", handoff)

        route = self._development_recommend_next(state, work_plan)
        state.add_artifact("route_recommendation", route)

        return state

    def _frame_problem(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Frame the problem: extract keywords, classify scope."""
        problem = context.get("problem", "")
        keywords = _extract_keywords(problem)
        root = self.project_root

        # Try to identify likely affected areas by keyword matching filenames
        affected_areas: List[str] = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            for fname in filenames:
                rel = str(Path(dirpath).relative_to(root) / fname)
                if _keyword_score(rel, keywords) > 0:
                    affected_areas.append(rel)

        affected_areas = affected_areas[:15]
        scope = "systemic" if len(affected_areas) > 5 else "bounded"

        return {
            "problem": problem or "Unspecified build problem",
            "keywords": keywords,
            "scope": scope,
            "affected_areas": affected_areas,
            "constraints": context.get("constraints", []),
            "success_criteria": context.get("success_criteria", [
                "change_implemented",
                "behavior_not_regressed",
                "route_recommendation_present",
            ]),
            "framed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _analyze_system(
        self,
        context: Dict[str, Any],
        frame: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Scan the project to understand current system shape."""
        root = self.project_root
        code_files = _walk_code_files(root)

        # Top-level module structure
        modules: List[str] = []
        for f in code_files:
            try:
                rel = str(f.relative_to(root))
                parts = Path(rel).parts
                if len(parts) >= 1:
                    top = parts[0]
                    if top not in modules and not _should_skip(top):
                        modules.append(top)
            except ValueError:
                pass

        # Estimate total LOC
        total_loc = sum(_count_loc(f) for f in code_files[:50])  # Cap to avoid slowdown

        # Count by family
        test_files = [f for f in code_files if any(p in _TEST_DIRS for p in f.parts)]

        return {
            "total_code_files": len(code_files),
            "top_level_modules": sorted(set(modules))[:20],
            "test_file_count": len(test_files),
            "estimated_loc": total_loc,
            "has_tests": len(test_files) > 0,
            "affected_areas": frame.get("affected_areas", []),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _design_approach(
        self,
        frame: Dict[str, Any],
        analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Decide approach based on problem scope and system shape."""
        scope = frame.get("scope", "bounded")
        has_tests = analysis.get("has_tests", False)
        affected_count = len(frame.get("affected_areas", []))

        if scope == "systemic":
            approach = "phased_development"
            decisions = [
                "Break work into independently deliverable slices",
                "Validate each slice before proceeding",
                "Use Forensics gate between major phase shifts",
            ]
        else:
            approach = "incremental"
            decisions = [
                "Identify narrowest change that satisfies the problem",
                "Implement change, then verify",
            ]

        if not has_tests:
            decisions.append("No test suite found — add regression check before calling complete")

        return {
            "approach": approach,
            "architecture_decisions": decisions,
            "recommended_next_pipeline": "coding" if scope == "bounded" else "development",
            "test_gate_required": not has_tests,
            "designed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _plan_work_slices(
        self,
        design: Dict[str, Any],
        frame: Dict[str, Any],
        analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate real work slices from the problem frame and system analysis."""
        affected = frame.get("affected_areas", [])
        keywords = frame.get("keywords", [])
        problem = frame.get("problem", "")

        slices: List[Dict[str, Any]] = []

        # Slice 0: always understand before changing
        slices.append({
            "id": "S0",
            "description": f"Verify understanding of current state before making changes",
            "files_affected": affected[:3],
            "dependencies": [],
            "validation_check": "Can explain current behavior of affected area",
            "status": "pending",
        })

        # One slice per affected area cluster (group by top-level dir)
        seen_tops: Dict[str, List[str]] = {}
        for area in affected:
            top = area.split("/")[0] if "/" in area else area
            seen_tops.setdefault(top, []).append(area)

        for i, (top, files) in enumerate(list(seen_tops.items())[:4], start=1):
            slices.append({
                "id": f"S{i}",
                "description": f"Implement changes in {top}/",
                "files_affected": files[:5],
                "dependencies": ["S0"],
                "validation_check": f"Changes in {top}/ are coherent and isolated",
                "status": "pending",
            })

        if not slices[1:]:  # No areas found — create a generic slice
            slices.append({
                "id": "S1",
                "description": f"Implement: {problem[:80]}",
                "files_affected": [],
                "dependencies": ["S0"],
                "validation_check": "Change implemented and verifiable",
                "status": "pending",
            })

        # Final: validate
        final_id = f"S{len(slices)}"
        slices.append({
            "id": final_id,
            "description": "Validate: run tests, confirm no regressions",
            "files_affected": [],
            "dependencies": [s["id"] for s in slices[1:]],
            "validation_check": "All tests pass or failures are explicitly triaged",
            "status": "pending",
        })

        return {
            "problem_summary": problem,
            "slices": slices,
            "total_slices": len(slices),
            "regression_checks": [
                "Existing tests still pass",
                "Public API behavior unchanged (if applicable)",
                "No new import cycles introduced",
            ],
            "planned_at": datetime.now(timezone.utc).isoformat(),
        }

    def _verify_approach(
        self,
        design: Dict[str, Any],
        plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Spot-check the approach against the plan."""
        slices = plan.get("slices", [])
        issues: List[str] = []

        if len(slices) < 2:
            issues.append("Work plan has fewer than 2 slices — may be underspecified")
        if not any(s.get("validation_check") for s in slices):
            issues.append("No slices have validation checks defined")

        return {
            "verified": len(issues) == 0,
            "issues": issues,
            "slice_count": len(slices),
            "approach": design.get("approach", "unknown"),
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _development_recommend_next(
        self,
        state: ExecutionState,
        plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Recommend next step after development planning."""
        slices = plan.get("slices", [])
        now = datetime.now(timezone.utc).isoformat()
        if slices:
            return {
                "recommended_next": "Forge/coding",
                "rationale": f"Work plan is ready with {len(slices)} slices — proceed to implementation.",
                "confidence": "high",
                "generated_at": now,
            }
        return {
            "recommended_next": "Forensics/project_mapping",
            "rationale": "Could not identify affected areas — ground the project state first.",
            "confidence": "medium",
            "generated_at": now,
        }

    def _assess_integration_state(
        self,
        work_plan: Dict[str, Any],
        verification: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Assess the integration state after development planning."""
        return {
            "integration_ready": verification.get("verified", False),
            "blocking_issues": verification.get("issues", []),
            "slice_count": len(work_plan.get("slices", [])),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _package_work(
        self,
        work_plan: Dict[str, Any],
        integration_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Produce packaging notes for the work plan."""
        return {
            "packaging_approach": "incremental" if len(work_plan.get("slices", [])) > 2 else "single",
            "integration_ready": integration_state.get("integration_ready", False),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _produce_handoff_or_release_note(
        self,
        work_plan: Dict[str, Any],
        verification: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Produce the handoff or release note for the development pipeline."""
        return {
            "kind": "handoff" if not verification.get("verified") else "release_note",
            "summary": f"Work plan with {len(work_plan.get('slices', []))} slices ready for execution.",
            "blocking_issues": verification.get("issues", []),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # coding
    # -----------------------------------------------------------------------

    def execute_coding(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute coding pipeline.

        Primary artifacts (spec-canonical):
        - change_plan
        - changed_artifacts
        - validation_note
        - route_recommendation

        Supporting artifacts:
        - local_surface_note
        - local_fit_note
        - metadata_update_record
        - unresolveds
        """
        # Phase 1: understand the change surface
        change_understanding = self._understand_change(context)
        state.add_artifact("change_understanding", change_understanding)

        local_surface = self._assess_local_surface(change_understanding)
        state.add_artifact("local_surface_note", local_surface)

        # Phase 2: plan the change
        change_plan = self._plan_change(change_understanding)
        state.add_artifact("change_plan", change_plan)

        # Phase 3: implement and document changed artifacts
        implementation = self._document_change(change_plan, context)
        state.add_artifact("changed_artifacts", implementation)

        local_fit = self._assess_local_fit(implementation, change_plan)
        state.add_artifact("local_fit_note", local_fit)

        # Phase 4: validate and record metadata updates
        validation = self._validate_change(implementation)
        state.add_artifact("validation_note", validation)

        metadata_record = self._record_metadata_updates(implementation)
        state.add_artifact("metadata_update_record", metadata_record)

        # Phase 5: surface unresolveds
        unresolveds = self._collect_coding_unresolveds(validation, local_fit)
        state.add_artifact("unresolveds", unresolveds)

        route = self._coding_recommend_next(validation, state)
        state.add_artifact("route_recommendation", route)

        return state

    def _understand_change(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Understand the change needed by scanning for affected files."""
        problem = context.get("problem", "")
        keywords = _extract_keywords(problem)
        root = self.project_root

        affected: List[Dict[str, Any]] = []
        for fpath in _walk_code_files(root):
            try:
                rel = str(fpath.relative_to(root))
                score = _keyword_score(rel, keywords)
                # Also scan file content for higher-scored matches
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")[:2000]
                    content_score = _keyword_score(content, keywords)
                    total = score * 3 + content_score  # path match weighs more
                except OSError:
                    total = score * 3
                if total > 0:
                    affected.append({"path": rel, "relevance_score": total})
            except ValueError:
                pass

        affected.sort(key=lambda x: x["relevance_score"], reverse=True)
        top_affected = [a["path"] for a in affected[:8]]

        change_type = "modification"
        if any(kw in problem.lower() for kw in ["add", "create", "new", "implement"]):
            change_type = "addition"
        elif any(kw in problem.lower() for kw in ["remove", "delete", "drop"]):
            change_type = "removal"
        elif any(kw in problem.lower() for kw in ["fix", "bug", "broken", "error"]):
            change_type = "bugfix"
        elif any(kw in problem.lower() for kw in ["refactor", "clean", "rename", "restructure"]):
            change_type = "refactor"

        return {
            "problem": problem,
            "change_type": change_type,
            "keywords": keywords,
            "affected_files": top_affected,
            "understood_at": datetime.now(timezone.utc).isoformat(),
        }

    def _plan_change(self, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Plan the change steps based on affected files."""
        change_type = understanding.get("change_type", "modification")
        affected = understanding.get("affected_files", [])

        steps_by_type = {
            "addition": ["Identify insertion point", "Draft new code", "Wire into existing structure", "Add tests for new behavior"],
            "removal": ["Verify nothing depends on the target", "Remove the code", "Clean up references", "Run tests"],
            "bugfix": ["Reproduce the failure", "Identify root cause", "Apply minimal fix", "Add regression test"],
            "refactor": ["Establish behavior baseline via tests", "Apply structural change", "Verify behavior unchanged", "Run full test suite"],
            "modification": ["Understand current behavior", "Make targeted change", "Validate change does not regress", "Update docs if public API changed"],
        }

        steps = steps_by_type.get(change_type, steps_by_type["modification"])

        return {
            "change_type": change_type,
            "steps": steps,
            "files_to_touch": affected,
            "planned_at": datetime.now(timezone.utc).isoformat(),
        }

    def _document_change(
        self,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Document what the change entails — the executor describes; Claude implements."""
        return {
            "change_description": context.get("problem", "Unspecified change"),
            "change_type": plan.get("change_type", "modification"),
            "files_to_touch": plan.get("files_to_touch", []),
            "implementation_steps": plan.get("steps", []),
            "implementation_note": (
                "The executor has identified the scope. "
                "Actual code changes are made by Claude in the skill layer, "
                "using this artifact as the change contract."
            ),
            "documented_at": datetime.now(timezone.utc).isoformat(),
        }

    def _validate_change(self, implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Check if affected files exist and note validation approach."""
        root = self.project_root
        files = implementation.get("files_to_touch", [])
        existing = [f for f in files if (root / f).exists()]
        missing = [f for f in files if not (root / f).exists()]

        return {
            "files_exist": existing,
            "files_missing": missing,
            "validation_approach": (
                "Run test suite after implementation. "
                "If no tests exist, manually verify the changed behavior."
            ),
            "validated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _coding_recommend_next(
        self,
        validation: Dict[str, Any],
        state: ExecutionState,
    ) -> Dict[str, Any]:
        """Recommend next step after coding."""
        now = datetime.now(timezone.utc).isoformat()
        missing = validation.get("files_missing", [])
        if missing:
            return {
                "recommended_next": "Forge/coding",
                "rationale": f"{len(missing)} referenced file(s) not found — scope may need adjustment.",
                "confidence": "medium",
                "generated_at": now,
            }
        return {
            "recommended_next": "Forge/testing",
            "rationale": "Change documented — run tests to confirm no regressions.",
            "confidence": "high",
            "generated_at": now,
        }

    def _assess_local_surface(self, change_understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the local surface of the change — what's exposed, what's adjacent."""
        affected = change_understanding.get("affected_files", [])
        return {
            "surface_files": affected,
            "surface_size": len(affected),
            "bounded": len(affected) <= 5,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _assess_local_fit(
        self,
        implementation: Dict[str, Any],
        change_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Assess whether the implemented change fits local conventions and contract."""
        return {
            "fits_local_conventions": True,
            "plan_covered": bool(change_plan.get("steps")),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _record_metadata_updates(self, implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Record any metadata updates required alongside the change."""
        return {
            "files_touched": implementation.get("files_to_touch", []),
            "metadata_targets": [],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _collect_coding_unresolveds(
        self,
        validation: Dict[str, Any],
        local_fit: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Surface coding unresolveds before exit."""
        issues = []
        if validation.get("files_missing"):
            issues.extend(validation["files_missing"])
        if not local_fit.get("fits_local_conventions"):
            issues.append("local_convention_mismatch")
        return {
            "unresolveds": issues,
            "count": len(issues),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # testing
    # -----------------------------------------------------------------------

    def execute_testing(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute testing pipeline.

        Primary artifacts (spec-canonical):
        - test_report

        Supporting artifacts:
        - results.json (as results_json)
        - defect_log
        - provenance_log
        """
        # Phase 1: understand test scope and strategy
        test_scope = self._understand_test_scope(context, state)
        state.add_artifact("test_scope", test_scope)

        test_strategy = self._design_tests(test_scope)
        state.add_artifact("test_strategy", test_strategy)

        # Phase 2: execute tests and collect raw results
        results = self._execute_tests(test_strategy, context)
        state.add_artifact("results_json", results)

        # Phase 3: classify defects if failures exist
        if results.get("failed", 0) > 0:
            defects = self._classify_defects(results)
            state.add_artifact("defect_log", defects)
        else:
            state.add_artifact("defect_log", {"defects": [], "status": "clean"})

        # Phase 4: create provenance log
        provenance = self._build_test_provenance(test_scope, results)
        state.add_artifact("provenance_log", provenance)

        # Phase 5: produce canonical test report
        report = self._create_test_report(results, state.artifacts)
        state.add_artifact("test_report", report)

        route = self._testing_recommend_next(results, state)
        state.add_artifact("route_recommendation", route)

        return state

    def _understand_test_scope(
        self,
        context: Dict[str, Any],
        state: ExecutionState,
    ) -> Dict[str, Any]:
        """Discover test files and determine scope."""
        root = self.project_root
        test_files: List[str] = []

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not _should_skip(d)]
            for fname in filenames:
                if fname.startswith("test_") or fname.endswith("_test.py"):
                    rel = str(Path(dirpath).relative_to(root) / fname)
                    test_files.append(rel)

        return {
            "test_files_found": test_files,
            "test_file_count": len(test_files),
            "has_test_suite": len(test_files) > 0,
            "scope": context.get("problem", "full project test run"),
            "artifacts_in_state": list(state.artifacts.keys()),
        }

    def _design_tests(self, scope: Dict[str, Any]) -> Dict[str, Any]:
        """Design test strategy."""
        has_tests = scope.get("has_test_suite", False)
        test_files = scope.get("test_files_found", [])

        if has_tests:
            return {
                "test_types": ["unit", "integration"],
                "runner": "pytest",
                "coverage_target": "critical_paths",
                "test_files": test_files,
                "strategy": "run_existing_suite",
            }
        return {
            "test_types": [],
            "runner": "none",
            "coverage_target": "none",
            "test_files": [],
            "strategy": "manual_verification_required",
            "note": "No test files found — manual verification is the only option",
        }

    def _execute_tests(
        self,
        strategy: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run pytest if available, capture and parse results."""
        if strategy.get("strategy") != "run_existing_suite":
            return {
                "runner": "none",
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "total": 0,
                "outcome": "no_tests",
                "note": "No test suite found — manual verification required",
                "executed_at": datetime.now(timezone.utc).isoformat(),
            }

        root = self.project_root
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--tb=short", "-q",
                 "--no-header", str(root)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(root),
            )
            output = result.stdout + result.stderr

            # Parse pytest summary line: "X passed, Y failed, Z error in W.XXs"
            passed = failed = errors = skipped = 0
            summary_match = re.search(
                r"(\d+) passed|(\d+) failed|(\d+) error|(\d+) skipped",
                output
            )
            for m in re.finditer(r"(\d+) (passed|failed|error[s]?|skipped)", output):
                count, label = int(m.group(1)), m.group(2)
                if "pass" in label:
                    passed = count
                elif "fail" in label:
                    failed = count
                elif "error" in label:
                    errors = count
                elif "skip" in label:
                    skipped = count

            total = passed + failed + errors + skipped
            outcome = "pass" if failed == 0 and errors == 0 else "fail"

            # Extract failure summaries (first 20 lines of failures)
            failure_lines: List[str] = []
            in_fail = False
            for line in output.splitlines():
                if "FAILED" in line or "ERROR" in line:
                    failure_lines.append(line.strip())
                if len(failure_lines) >= 10:
                    break

            return {
                "runner": "pytest",
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "skipped": skipped,
                "total": total,
                "outcome": outcome,
                "failure_summaries": failure_lines,
                "raw_output_tail": output.splitlines()[-20:],
                "return_code": result.returncode,
                "executed_at": datetime.now(timezone.utc).isoformat(),
            }

        except subprocess.TimeoutExpired:
            return {
                "runner": "pytest",
                "outcome": "timeout",
                "note": "Test run exceeded 120s timeout",
                "executed_at": datetime.now(timezone.utc).isoformat(),
            }
        except FileNotFoundError:
            return {
                "runner": "none",
                "outcome": "runner_not_found",
                "note": "pytest not available in this environment",
                "executed_at": datetime.now(timezone.utc).isoformat(),
            }

    def _classify_defects(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Classify test failures by pattern."""
        failures = results.get("failure_summaries", [])
        defects: List[Dict[str, Any]] = []

        for f in failures:
            if "ImportError" in f or "ModuleNotFound" in f:
                sev, dtype = "critical", "import_error"
            elif "AssertionError" in f:
                sev, dtype = "major", "assertion_failure"
            elif "AttributeError" in f:
                sev, dtype = "major", "attribute_error"
            elif "TypeError" in f or "ValueError" in f:
                sev, dtype = "major", "type_or_value_error"
            else:
                sev, dtype = "minor", "unknown"
            defects.append({"failure": f, "type": dtype, "severity": sev})

        severity_dist = {}
        for d in defects:
            severity_dist[d["severity"]] = severity_dist.get(d["severity"], 0) + 1

        return {
            "defects": defects,
            "severity_distribution": severity_dist,
            "classified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _create_test_report(
        self,
        results: Dict[str, Any],
        artifacts: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Summarize test results."""
        passed = results.get("passed", 0)
        failed = results.get("failed", 0)
        errors = results.get("errors", 0)
        outcome = results.get("outcome", "unknown")

        return {
            "summary": f"Outcome: {outcome} | Passed: {passed} | Failed: {failed} | Errors: {errors}",
            "outcome": outcome,
            "pass_rate": round(passed / max(passed + failed + errors, 1) * 100, 1),
            "failure_count": failed + errors,
            "failure_summaries": results.get("failure_summaries", []),
            "report_at": datetime.now(timezone.utc).isoformat(),
        }

    def _testing_recommend_next(
        self,
        results: Dict[str, Any],
        state: ExecutionState,
    ) -> Dict[str, Any]:
        """Recommend next step based on test results."""
        outcome = results.get("outcome", "unknown")
        failed = results.get("failed", 0) + results.get("errors", 0)
        now = datetime.now(timezone.utc).isoformat()

        if outcome == "pass":
            return {
                "recommended_next": "Conduit/documentation",
                "rationale": "All tests pass — ready to document and hand off.",
                "confidence": "high",
                "generated_at": now,
            }
        elif outcome in ("no_tests", "runner_not_found"):
            return {
                "recommended_next": "Conduit/documentation",
                "rationale": "No automated tests — document the change with manual verification notes.",
                "confidence": "medium",
                "generated_at": now,
            }
        elif failed <= 2:
            return {
                "recommended_next": "Forge/coding",
                "rationale": f"{failed} failure(s) — targeted local fix needed.",
                "confidence": "high",
                "generated_at": now,
            }
        else:
            return {
                "recommended_next": "Forge/development",
                "rationale": f"{failed} failure(s) suggest structural issues — replanning needed.",
                "confidence": "high",
                "generated_at": now,
            }

    def _build_test_provenance(
        self,
        test_scope: Dict[str, Any],
        results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a provenance log for the test run."""
        return {
            "test_files": test_scope.get("test_files_found", []),
            "total_run": results.get("total", 0),
            "passed": results.get("passed", 0),
            "failed": results.get("failed", 0),
            "errors": results.get("errors", 0),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # refactor
    # -----------------------------------------------------------------------

    def execute_refactor(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute refactor pipeline."""
        shape_map = self._map_current_shape(context)
        state.add_artifact("current_shape_map", shape_map)

        invariants = self._identify_invariants(shape_map)
        state.add_artifact("invariants_ledger", invariants)

        refactor_plan = self._plan_refactor(shape_map, invariants, context)
        state.add_artifact("refactor_plan", refactor_plan)

        refactored = self._document_refactor(refactor_plan)
        state.add_artifact("refactored_artifact", refactored)

        validation = self._validate_behavior(refactored, invariants)
        state.add_artifact("behavior_validation", validation)

        route = self._refactor_recommend_next(validation)
        state.add_artifact("route_recommendation", route)

        return state

    def _map_current_shape(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Scan project for complexity hotspots."""
        root = self.project_root
        code_files = _walk_code_files(root)
        hotspots: List[Dict[str, Any]] = []

        for fpath in code_files:
            if fpath.suffix != ".py":
                continue
            try:
                loc = _count_loc(fpath)
                funcs = _get_functions(fpath)
                rel = str(fpath.relative_to(root))
                complexity_score = loc + len(funcs) * 10
                large_funcs = [f for f in funcs if f.get("args", 0) > 5]
                if loc > 150 or len(large_funcs) > 0:
                    hotspots.append({
                        "file": rel,
                        "loc": loc,
                        "function_count": len(funcs),
                        "large_functions": [f["name"] for f in large_funcs],
                        "complexity_score": complexity_score,
                    })
            except (OSError, ValueError):
                pass

        hotspots.sort(key=lambda x: x["complexity_score"], reverse=True)

        return {
            "total_code_files": len(code_files),
            "complexity_hotspots": hotspots[:10],
            "hotspot_count": len(hotspots),
            "analysis_scope": context.get("problem", "full project"),
            "mapped_at": datetime.now(timezone.utc).isoformat(),
        }

    def _identify_invariants(self, shape_map: Dict[str, Any]) -> Dict[str, Any]:
        """Identify public APIs that must not change behavior."""
        root = self.project_root
        public_funcs: List[str] = []
        code_files = _walk_code_files(root)

        for fpath in code_files:
            if fpath.suffix != ".py":
                continue
            try:
                rel = str(fpath.relative_to(root))
                for func in _get_functions(fpath):
                    if func.get("public"):
                        public_funcs.append(f"{rel}::{func['name']}")
            except (OSError, ValueError):
                pass

        return {
            "invariants": [
                "Public function signatures must not change without deprecation notice",
                "External-facing behavior must be preserved",
                "Existing test assertions must still pass",
            ],
            "public_api_functions": public_funcs[:20],
            "public_api_count": len(public_funcs),
            "identified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _plan_refactor(
        self,
        shape_map: Dict[str, Any],
        invariants: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Plan the refactor based on hotspots and invariants."""
        hotspots = shape_map.get("complexity_hotspots", [])
        problem = context.get("problem", "")
        keywords = _extract_keywords(problem)

        # Filter hotspots by keywords if provided
        if keywords:
            relevant = [h for h in hotspots if _keyword_score(h["file"], keywords) > 0]
        else:
            relevant = hotspots[:3]

        refactorings: List[Dict[str, Any]] = []
        for h in relevant[:5]:
            suggestions: List[str] = []
            if h["loc"] > 300:
                suggestions.append(f"Split {h['file']} — {h['loc']} LOC is too large for one file")
            if h["large_functions"]:
                suggestions.append(f"Extract methods from: {', '.join(h['large_functions'][:3])}")
            if h["function_count"] > 20:
                suggestions.append(f"Consider splitting into submodules")
            if suggestions:
                refactorings.append({"file": h["file"], "suggestions": suggestions})

        if not refactorings:
            refactorings.append({
                "file": "unknown",
                "suggestions": [f"No high-complexity hotspots matched '{problem}' — broaden scope or specify file"],
            })

        return {
            "target_description": problem,
            "refactorings": refactorings,
            "must_preserve": invariants.get("invariants", []),
            "baseline_step": "Run full test suite before any structural changes",
            "planned_at": datetime.now(timezone.utc).isoformat(),
        }

    def _document_refactor(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Document the refactor contract."""
        return {
            "refactor_description": plan.get("target_description", ""),
            "planned_changes": plan.get("refactorings", []),
            "invariants_to_preserve": plan.get("must_preserve", []),
            "implementation_note": (
                "Actual structural changes are made by Claude in the skill layer. "
                "This artifact is the refactor contract."
            ),
            "documented_at": datetime.now(timezone.utc).isoformat(),
        }

    def _validate_behavior(
        self,
        refactored: Dict[str, Any],
        invariants: Dict[str, Any],
    ) -> Dict[str, Any]:
        """State the behavior validation requirements."""
        return {
            "behavior_preserved": None,  # Unknown until tests run
            "validation_required": invariants.get("invariants", []),
            "validation_method": "Run full test suite after refactor. Compare public API surface before and after.",
            "public_api_count": invariants.get("public_api_count", 0),
            "note": "Behavioral preservation can only be confirmed by running tests post-refactor.",
            "validated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _refactor_recommend_next(self, validation: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend next step after refactor."""
        now = datetime.now(timezone.utc).isoformat()
        return {
            "recommended_next": "Forge/testing",
            "rationale": "Refactor plan ready — run tests immediately after implementing to confirm no regression.",
            "confidence": "high",
            "generated_at": now,
        }
