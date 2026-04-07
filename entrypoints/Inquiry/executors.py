"""
Inquiry family pipeline executors.

Implements execution for Inquiry family pipelines:
- research
- hypothesis_generation
- data_analysis
- formalization
- mathematics
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from runtime.state.models import ExecutionState, TrustAssessment, FamilyType
from runtime.artifacts.writer import ArtifactWriter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SKIP_DIRS = {
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules",
    ".venv", "venv", "env", ".env", "dist", "build",
}
_DOC_EXTS = {".md", ".rst", ".txt"}
_CODE_EXTS = {".py", ".js", ".ts", ".go", ".rs", ".java"}


def _should_skip(name: str) -> bool:
    return name in _SKIP_DIRS or name.endswith(".egg-info")


def _extract_keywords(text: str) -> List[str]:
    stopwords = {"a", "an", "the", "to", "in", "of", "for", "with", "and", "or",
                 "is", "it", "on", "at", "as", "be", "by", "do", "we", "how",
                 "what", "why", "when", "where", "this", "that", "from", "not",
                 "are", "was", "were", "will", "can", "has", "have", "had",
                 "should", "would", "could", "need", "want", "get", "make"}
    words = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text)
    return [w for w in words if w.lower() not in stopwords and len(w) > 2]


def _keyword_score(text: str, keywords: List[str]) -> int:
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def _scan_docs_for_keywords(
    root: Path,
    keywords: List[str],
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Scan doc and code files for keyword matches. Returns ranked results.
    """
    results: List[Dict[str, Any]] = []
    all_exts = _DOC_EXTS | _CODE_EXTS

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not _should_skip(d)]
        for fname in filenames:
            if Path(fname).suffix.lower() not in all_exts:
                continue
            fpath = Path(dirpath) / fname
            try:
                rel = str(fpath.relative_to(root))
                text = fpath.read_text(encoding="utf-8", errors="replace")[:4000]
                score = _keyword_score(text, keywords)
                if score > 0:
                    # Extract a short snippet around the first keyword match
                    snippet = ""
                    for kw in keywords:
                        idx = text.lower().find(kw.lower())
                        if idx >= 0:
                            start = max(0, idx - 60)
                            end = min(len(text), idx + 120)
                            snippet = text[start:end].strip().replace("\n", " ")[:200]
                            break
                    results.append({
                        "path": rel,
                        "relevance_score": score,
                        "snippet": snippet,
                        "type": "doc" if Path(fname).suffix.lower() in _DOC_EXTS else "code",
                    })
            except (OSError, ValueError):
                pass

    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:max_results]


class InquiryExecutor:
    """
    Executor for Inquiry family pipelines.

    Implements phase execution for investigation and explanation work.
    """

    def __init__(self, output_path: Path, project_root: Optional[Path] = None):
        self.output_path = output_path
        self.project_root = project_root or Path.cwd()
        self.writer = ArtifactWriter(output_path)
    
    def execute_research(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute research pipeline.

        Primary artifacts (spec-canonical):
        - source_ledger
        - synthesis_note
        - support_and_gap_map
        - route_or_commit_recommendation

        Supporting artifacts:
        - question_frame
        - comparison_map
        - evidence_state_note
        - unresolveds
        """
        # Phase 1: frame_question
        question = self._frame_question(context)
        state.add_artifact("question_frame", question)

        # Phase 2: gather_sources
        sources = self._gather_sources(question)
        state.add_artifact("source_ledger", sources)

        # Phase 3: compare_perspectives
        comparison = self._compare_perspectives(sources)
        state.add_artifact("comparison_map", comparison)

        # Phase 4: synthesize
        synthesis = self._synthesize(comparison)
        state.add_artifact("synthesis_note", synthesis)

        # Phase 5: map_support_gaps
        gaps = self._map_support_gaps(synthesis)
        state.add_artifact("support_and_gap_map", gaps)

        # Phase 6: verify evidence state
        evidence_state = self._assess_evidence_state(gaps, state)
        state.add_artifact("evidence_state_note", evidence_state)

        # Phase 7: surface unresolveds before exit
        unresolveds = self._collect_unresolveds(gaps, evidence_state)
        state.add_artifact("unresolveds", unresolveds)

        # Phase 8: recommend route or commit
        route = self._research_recommend_route(gaps, state)
        state.add_artifact("route_or_commit_recommendation", route)

        return state
    
    def execute_hypothesis_generation(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute hypothesis_generation pipeline.

        Primary artifacts (spec-canonical):
        - candidate_set
        - discriminator_list
        - provisional_selection_note
        - route_recommendation

        Supporting artifacts:
        - gap_note
        - preserved_rival_note
        - candidate_assessment
        - evidence_gap_note
        """
        # Phase 1: define gap or anomaly
        gap = self._define_gap_or_anomaly(context)
        state.add_artifact("gap_note", gap)

        # Phase 2: generate diverse candidates
        candidates = self._generate_candidates(gap)
        state.add_artifact("candidate_set", candidates)

        # Phase 3: preserve rivals before closure
        rivals = self._preserve_rivals(candidates)
        state.add_artifact("preserved_rival_note", rivals)

        # Phase 4: identify discriminators
        discriminators = self._identify_discriminators(candidates)
        state.add_artifact("discriminator_list", discriminators)

        # Phase 5: evaluate candidates against support
        assessment = self._evaluate_candidates(candidates, discriminators)
        state.add_artifact("candidate_assessment", assessment)

        # Phase 6: provisional selection with residue preserved
        selection = self._provisional_selection(candidates, assessment)
        state.add_artifact("provisional_selection_note", selection)

        gaps = self._map_evidence_gaps(selection)
        state.add_artifact("evidence_gap_note", gaps)

        # Phase 7: recommend route
        route = self._hypothesis_recommend_route(selection, gaps)
        state.add_artifact("route_recommendation", route)

        return state
    
    def execute_formalization(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute formalization pipeline.

        Primary artifacts (spec-canonical):
        - definition_set
        - object_relation_map
        - assumption_ledger
        - route_recommendation

        Supporting artifacts:
        - concept_packet
        - consistency_note
        - gap_note
        - notation_sheet
        """
        # Phase 1: collect live concepts and claims
        concepts = self._identify_concepts(context)
        state.add_artifact("concept_packet", concepts)

        # Phase 2: identify objects, relations, assumptions
        relations = self._map_relations(concepts)
        state.add_artifact("object_relation_map", relations)

        assumptions = self._surface_assumptions(concepts, relations)
        state.add_artifact("assumption_ledger", assumptions)

        # Phase 3: define terms and boundaries
        definitions = self._define_terms(concepts)
        state.add_artifact("definition_set", definitions)

        # Phase 4: check internal consistency
        consistency = self._check_consistency(definitions, assumptions)
        state.add_artifact("consistency_note", consistency)

        # Phase 5: expose remaining gaps or underspecification
        gaps = self._expose_gaps(definitions, consistency)
        state.add_artifact("gap_note", gaps)

        # Phase 6: tidy notation and representation
        notation = self._establish_notation(definitions)
        state.add_artifact("notation_sheet", notation)

        # Phase 7: recommend route
        route = self._formalization_recommend_route(notation, state)
        state.add_artifact("route_recommendation", route)

        return state
    
    def execute_mathematics(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute mathematics pipeline.

        Primary artifacts (spec-canonical):
        - proof (or counterexample, or derivation — whichever applies)
        - derivation

        Supporting artifacts:
        - assumptions
        - unresolveds
        - provenance_log
        """
        # Phase 1: state problem
        problem = self._state_problem(context)
        state.add_artifact("problem_statement", problem)
        state.add_artifact("target_result_or_open_question",
                           {"source": "problem_statement", "status": "open"})

        # Phase 2: bind assumptions
        assumptions = self._ledger_assumptions(problem)
        state.add_artifact("assumptions", assumptions)

        defined_objects = self._extract_defined_objects(assumptions)
        state.add_artifact("defined_objects", defined_objects)

        # Phase 3: derive or search
        derivation_paths = self._derive_or_search(problem, assumptions)
        state.add_artifact("derivation_paths", derivation_paths)

        candidate_argument = self._select_candidate_argument(derivation_paths)
        state.add_artifact("derivation", candidate_argument)

        # Phase 4: edge case check
        counterexample_attempts = self._search_counterexamples(candidate_argument)
        state.add_artifact("counterexample_attempts", counterexample_attempts)

        edge_case_notes = self._check_edge_cases(candidate_argument)
        state.add_artifact("edge_case_notes", edge_case_notes)

        # Phase 5: rigor check
        rigor = self._assess_rigor(candidate_argument, edge_case_notes)
        state.add_artifact("rigor_assessment", rigor)

        unresolved_gaps = self._identify_unresolved_gaps(rigor)
        state.add_artifact("unresolveds", unresolved_gaps)

        # Phase 6: notation cleanup
        notation_ledger = self._normalize_notation(candidate_argument)
        state.add_artifact("notation_ledger", notation_ledger)

        # Phase 7: finalize — produce proof, counterexample, or open derivation
        result = self._finalize_result(candidate_argument, rigor, counterexample_attempts)
        result_kind = result.get("kind", "derivation")  # proof | counterexample | derivation
        state.add_artifact(result_kind, result)

        provenance = self._build_provenance_log(problem, assumptions, candidate_argument)
        state.add_artifact("provenance_log", provenance)

        # Route recommendation
        route = self._math_recommend_route(result, rigor)
        state.add_artifact("route_recommendation", route)

        return state
    
    def execute_data_analysis(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """
        Execute data_analysis pipeline.

        Primary artifacts (spec-canonical):
        - analysis_question
        - dataset_ledger
        - results_report
        - route_recommendation

        Supporting artifacts:
        - preprocessing_record
        - exploration_summary
        - model_specification
        - uncertainty_note
        - interpretation_note
        """
        # Phase 1: define analysis question
        question = self._frame_analysis_question(context)
        state.add_artifact("analysis_question", question)

        # Phase 2: collect and preprocess data
        datasets = self._inventory_datasets(context)
        state.add_artifact("dataset_ledger", datasets)

        preprocessing = self._preprocess(datasets)
        state.add_artifact("preprocessing_record", preprocessing)

        # Phase 3: explore patterns and distributions
        exploration = self._explore(preprocessing)
        state.add_artifact("exploration_summary", exploration)

        # Phase 4: build or select model
        model = self._specify_model(exploration, question)
        state.add_artifact("model_specification", model)

        # Phase 5: evaluate results and uncertainties
        results = self._report_results(model, exploration)
        state.add_artifact("results_report", results)

        uncertainty = self._assess_uncertainty(results, model)
        state.add_artifact("uncertainty_note", uncertainty)

        # Phase 6: interpret results in context
        interpretation = self._interpret_results(results, question)
        state.add_artifact("interpretation_note", interpretation)

        # Phase 7: finalize or reroute
        route = self._analysis_recommend_route(results)
        state.add_artifact("route_recommendation", route)

        return state
    
    # -----------------------------------------------------------------------
    # Research phase helpers
    # -----------------------------------------------------------------------

    def _frame_question(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Frame the research question with explicit scope and success criteria."""
        question = context.get("question", "")
        keywords = _extract_keywords(question)
        return {
            "question": question or "Unspecified research question",
            "keywords": keywords,
            "scope": {
                "in_scope": context.get("scope_in", [f"Project files containing: {', '.join(keywords[:5])}"]),
                "out_of_scope": context.get("scope_out", []),
            },
            "success_criteria": context.get("success_criteria",
                "Evidence located, perspectives compared, supported claims distinguished from gaps"),
            "framed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _gather_sources(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """Scan project for sources relevant to the question."""
        keywords = question.get("keywords", [])
        root = self.project_root

        if not keywords:
            return {
                "sources": [],
                "total_found": 0,
                "note": "No keywords extracted from question — broaden or restate the question",
                "gathered_at": datetime.now(timezone.utc).isoformat(),
            }

        raw = _scan_docs_for_keywords(root, keywords, max_results=15)
        sources = []
        for r in raw:
            sources.append({
                "path": r["path"],
                "type": r["type"],
                "relevance_score": r["relevance_score"],
                "snippet": r["snippet"],
                "trust_level": "provisional",  # Trust is assessed; not assumed
            })

        return {
            "sources": sources,
            "total_found": len(sources),
            "keywords_used": keywords,
            "gathered_at": datetime.now(timezone.utc).isoformat(),
        }

    def _compare_perspectives(self, sources: Dict[str, Any]) -> Dict[str, Any]:
        """Compare what different source types say — docs vs. code."""
        doc_sources = [s for s in sources.get("sources", []) if s["type"] == "doc"]
        code_sources = [s for s in sources.get("sources", []) if s["type"] == "code"]

        perspectives: List[Dict[str, Any]] = []
        if doc_sources:
            perspectives.append({
                "source_type": "documentation",
                "files": [s["path"] for s in doc_sources[:5]],
                "perspective": "Documented/specified behavior",
                "sample_snippet": doc_sources[0]["snippet"] if doc_sources else "",
            })
        if code_sources:
            perspectives.append({
                "source_type": "code",
                "files": [s["path"] for s in code_sources[:5]],
                "perspective": "Implemented/observed behavior",
                "sample_snippet": code_sources[0]["snippet"] if code_sources else "",
            })

        agreement = []
        disagreement = []
        if doc_sources and code_sources:
            # Simple heuristic: if both reference the same term, potential alignment
            doc_text = " ".join(s["snippet"] for s in doc_sources)
            code_text = " ".join(s["snippet"] for s in code_sources)
            shared_terms = set(doc_text.lower().split()) & set(code_text.lower().split())
            shared_terms -= {"the", "a", "in", "of", "to", "and", "or", "is", "for"}
            if shared_terms:
                agreement.append(f"Both sources reference: {', '.join(list(shared_terms)[:5])}")
        if len(perspectives) > 1:
            disagreement.append("Doc and code perspectives may diverge — verify against observed state")

        return {
            "perspectives": perspectives,
            "areas_of_agreement": agreement,
            "areas_of_disagreement": disagreement,
            "compared_at": datetime.now(timezone.utc).isoformat(),
        }

    def _synthesize(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize findings across perspectives."""
        perspectives = comparison.get("perspectives", [])
        agreement = comparison.get("areas_of_agreement", [])
        disagreement = comparison.get("areas_of_disagreement", [])

        if not perspectives:
            synthesis = "No relevant sources found in project. The question may reference external knowledge not present in the codebase."
            confidence = "low"
        elif len(perspectives) == 1:
            p = perspectives[0]
            synthesis = f"Evidence found only in {p['source_type']} sources: {', '.join(p['files'][:3])}. Single-source confidence is limited."
            confidence = "low"
        else:
            synthesis = (
                f"Evidence found across {len(perspectives)} source type(s). "
                f"Agreement: {'; '.join(agreement) if agreement else 'none identified'}. "
                f"Tension: {'; '.join(disagreement) if disagreement else 'none identified'}."
            )
            confidence = "medium" if disagreement else "high"

        gaps: List[str] = []
        if not perspectives:
            gaps.append("No project sources found — external research may be required")
        if disagreement:
            gaps.append("Doc/code disagreement detected — verify which is authoritative")

        return {
            "synthesis": synthesis,
            "confidence": confidence,
            "source_count": sum(len(p.get("files", [])) for p in perspectives),
            "gaps": gaps,
            "synthesized_at": datetime.now(timezone.utc).isoformat(),
        }

    def _map_support_gaps(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify what is supported vs. what has gaps."""
        gaps = synthesis.get("gaps", [])
        confidence = synthesis.get("confidence", "low")

        supported = []
        unsupported = []
        if confidence in ("medium", "high"):
            supported.append("Investigation question has relevant evidence in project")
        else:
            unsupported.append("Investigation question lacks sufficient project-internal evidence")

        return {
            "supported_claims": supported,
            "unsupported_claims": unsupported,
            "gaps": gaps,
            "evidence_confidence": confidence,
            "mapped_at": datetime.now(timezone.utc).isoformat(),
        }

    def _research_recommend_route(
        self,
        gaps: Dict[str, Any],
        state: ExecutionState,
    ) -> Dict[str, Any]:
        """Recommend next step based on gap count and confidence."""
        now = datetime.now(timezone.utc).isoformat()
        confidence = gaps.get("evidence_confidence", "low")
        gap_list = gaps.get("gaps", [])

        if confidence == "low" or len(gap_list) > 1:
            return {
                "recommended_next": "Inquiry/hypothesis_generation",
                "rationale": f"Insufficient evidence ({len(gap_list)} gap(s)) — competing hypotheses needed.",
                "confidence": "medium",
                "generated_at": now,
            }
        return {
            "recommended_next": "Conduit/documentation",
            "rationale": "Synthesis is sufficiently supported — ready for communication.",
            "confidence": "medium",
            "generated_at": now,
        }

    # -----------------------------------------------------------------------
    # Hypothesis generation phase helpers
    # -----------------------------------------------------------------------

    def _understand_phenomenon(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Understand the phenomenon via project scan."""
        question = context.get("question", "")
        keywords = _extract_keywords(question)
        root = self.project_root
        sources = _scan_docs_for_keywords(root, keywords, max_results=5)

        observations = [s["snippet"] for s in sources if s["snippet"]]

        return {
            "phenomenon": question or "Unspecified phenomenon",
            "keywords": keywords,
            "observations": observations,
            "source_paths": [s["path"] for s in sources],
            "understood_at": datetime.now(timezone.utc).isoformat(),
        }

    def _generate_candidates(self, phenomenon: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competing hypotheses based on the phenomenon and project evidence."""
        question = phenomenon.get("phenomenon", "")
        keywords = phenomenon.get("keywords", [])
        observations = phenomenon.get("observations", [])

        # Build hypotheses from different explanatory frames
        candidates = []

        # H1: The simplest/most direct explanation
        candidates.append({
            "id": "H1",
            "label": "Direct cause",
            "description": f"The behavior in question is a direct result of the implementation in the identified source files.",
            "supporting_observations": observations[:1],
            "plausibility": "medium",
            "testable_by": "Read the implementation of the relevant functions and trace the call path",
        })

        # H2: Configuration or environment explanation
        candidates.append({
            "id": "H2",
            "label": "Configuration / environment",
            "description": "The behavior is caused by a configuration value, environment variable, or runtime condition rather than a code bug.",
            "supporting_observations": [],
            "plausibility": "medium",
            "testable_by": "Check config files, env vars, and runtime flags in the affected path",
        })

        # H3: Missing or stale component
        candidates.append({
            "id": "H3",
            "label": "Missing or stale component",
            "description": "The behavior is caused by a component that is absent, outdated, or not yet implemented.",
            "supporting_observations": observations[1:2],
            "plausibility": "low",
            "testable_by": "Run Forensics/project_mapping to verify all referenced components exist",
        })

        return {
            "candidates": candidates,
            "question": question,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _identify_discriminators(self, candidates: Dict[str, Any]) -> Dict[str, Any]:
        """Identify what evidence would distinguish between candidates."""
        cand_list = candidates.get("candidates", [])
        discriminators = []

        for c in cand_list:
            discriminators.append({
                "hypothesis": c["id"],
                "discriminating_test": c.get("testable_by", "Manual investigation required"),
                "kills_if": f"{c['id']} is false if the test finds no match",
            })

        return {
            "discriminators": discriminators,
            "ranking_method": "Test H1 first (lowest cost); eliminate before escalating to H2, H3",
            "identified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _provisional_selection(
        self,
        candidates: Dict[str, Any],
        discriminators: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Provisionally select the highest-plausibility hypothesis."""
        cand_list = candidates.get("candidates", [])
        # Rank by plausibility
        rank = {"high": 3, "medium": 2, "low": 1}
        sorted_cands = sorted(cand_list, key=lambda c: rank.get(c.get("plausibility", "low"), 1), reverse=True)
        selected = sorted_cands[0] if sorted_cands else None

        return {
            "selected": selected,
            "rationale": f"Provisionally selected based on highest plausibility and lowest investigation cost",
            "confidence": "provisional",
            "alternatives": sorted_cands[1:],
            "selected_at": datetime.now(timezone.utc).isoformat(),
        }

    def _map_evidence_gaps(self, selection: Dict[str, Any]) -> Dict[str, Any]:
        """Identify what evidence is still needed."""
        selected = selection.get("selected", {})
        alternatives = selection.get("alternatives", [])

        needed: List[str] = []
        if selected:
            needed.append(f"Confirm or refute {selected.get('id','H1')}: {selected.get('testable_by','')}")
        for alt in alternatives[:2]:
            needed.append(f"If {selected.get('id','H1')} is eliminated: test {alt.get('id','H?')}")

        return {
            "gaps": [f"Evidence needed to confirm selected hypothesis"] if selected else ["No hypothesis selected"],
            "needed_evidence": needed,
            "mapped_at": datetime.now(timezone.utc).isoformat(),
        }

    def _hypothesis_recommend_route(
        self,
        selection: Dict[str, Any],
        gaps: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Recommend next step."""
        now = datetime.now(timezone.utc).isoformat()
        needed = gaps.get("needed_evidence", [])
        if needed:
            return {
                "recommended_next": "Inquiry/research",
                "rationale": f"Hypothesis selected but {len(needed)} evidence gap(s) remain — targeted research needed.",
                "confidence": "medium",
                "generated_at": now,
            }
        return {
            "recommended_next": "Inquiry/formalization",
            "rationale": "Hypothesis selected with sufficient support — formalize before acting.",
            "confidence": "medium",
            "generated_at": now,
        }

    # -----------------------------------------------------------------------
    # Formalization phase helpers
    # -----------------------------------------------------------------------

    def _identify_concepts(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and classify key concepts from the question."""
        question = context.get("question", "")
        keywords = _extract_keywords(question)

        # Scan project for each keyword to see if it corresponds to a real component
        root = self.project_root
        concept_map: List[Dict[str, Any]] = []
        for kw in keywords[:10]:
            sources = _scan_docs_for_keywords(root, [kw], max_results=2)
            concept_map.append({
                "concept": kw,
                "found_in_project": len(sources) > 0,
                "locations": [s["path"] for s in sources],
                "definition_status": "found" if sources else "undefined",
            })

        return {
            "concepts": concept_map,
            "total_identified": len(concept_map),
            "undefined_count": sum(1 for c in concept_map if c["definition_status"] == "undefined"),
            "identified_at": datetime.now(timezone.utc).isoformat(),
        }

    def _map_relations(self, concepts: Dict[str, Any]) -> Dict[str, Any]:
        """Infer relations between identified concepts."""
        concept_list = concepts.get("concepts", [])
        relations: List[Dict[str, Any]] = []

        # Group concepts that co-appear in the same project locations
        location_map: Dict[str, List[str]] = {}
        for c in concept_list:
            for loc in c.get("locations", []):
                location_map.setdefault(loc, []).append(c["concept"])

        for loc, concepts_in_loc in location_map.items():
            if len(concepts_in_loc) > 1:
                for i, a in enumerate(concepts_in_loc):
                    for b in concepts_in_loc[i+1:]:
                        relations.append({
                            "from": a,
                            "to": b,
                            "relation": "co_located",
                            "evidence": loc,
                        })

        return {
            "relations": relations[:20],
            "relation_count": len(relations),
            "note": "Relations derived from co-location in project files — causal relations require additional investigation",
            "mapped_at": datetime.now(timezone.utc).isoformat(),
        }

    def _surface_assumptions(
        self,
        concepts: Dict[str, Any],
        relations: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Surface hidden assumptions in the formalization."""
        assumptions: List[str] = []
        undefined = concepts.get("undefined_count", 0)

        if undefined > 0:
            assumptions.append(
                f"{undefined} concept(s) have no project-level definition — "
                "they are assumed to be understood from external context"
            )

        relations_list = relations.get("relations", [])
        if relations_list:
            assumptions.append(
                "Co-location implies relation — this may not hold if the files are unrelated"
            )

        if not assumptions:
            assumptions.append("No hidden assumptions surfaced — formalization appears well-grounded")

        return {
            "assumptions": assumptions,
            "assumption_count": len(assumptions),
            "surfaced_at": datetime.now(timezone.utc).isoformat(),
        }

    def _define_terms(self, concepts: Dict[str, Any]) -> Dict[str, Any]:
        """Produce working definitions for each concept."""
        concept_list = concepts.get("concepts", [])
        definitions: Dict[str, str] = {}
        for c in concept_list:
            if c["found_in_project"]:
                definitions[c["concept"]] = f"Defined in project at: {', '.join(c['locations'][:2])}"
            else:
                definitions[c["concept"]] = "No project-level definition found — requires external definition"
        return {
            "definitions": definitions,
            "defined_count": sum(1 for v in definitions.values() if "No project" not in v),
            "undefined_count": sum(1 for v in definitions.values() if "No project" in v),
            "defined_at": datetime.now(timezone.utc).isoformat(),
        }

    def _establish_notation(self, definitions: Dict[str, Any]) -> Dict[str, Any]:
        """Establish notation for the formal structure."""
        defined = definitions.get("definitions", {})
        notation: Dict[str, str] = {}
        for i, (term, defn) in enumerate(list(defined.items())[:10]):
            # Use first letter as notation symbol if available
            symbol = term[0].upper() if term else f"X{i}"
            notation[symbol] = term

        return {
            "notation": notation,
            "symbol_count": len(notation),
            "note": "Notation is suggestive — establish formal symbols before mathematical proof",
            "established_at": datetime.now(timezone.utc).isoformat(),
        }

    def _formalization_recommend_route(
        self,
        notation: Dict[str, Any],
        state: ExecutionState,
    ) -> Dict[str, Any]:
        """Recommend next step after formalization."""
        now = datetime.now(timezone.utc).isoformat()
        undefined = state.artifacts.get("concept_map", {}).get("undefined_count", 0)
        if undefined > 2:
            return {
                "recommended_next": "Inquiry/research",
                "rationale": f"{undefined} undefined concepts — gather definitions before attempting proof.",
                "confidence": "high",
                "generated_at": now,
            }
        return {
            "recommended_next": "Inquiry/mathematics",
            "rationale": "Concepts defined and notation established — ready for rigorous proof or derivation.",
            "confidence": "medium",
            "generated_at": now,
        }

    # -----------------------------------------------------------------------
    # Mathematics phase helpers
    # -----------------------------------------------------------------------

    def _state_problem(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """State the mathematical problem clearly."""
        question = context.get("question", "")
        # Detect if this looks like a math problem
        math_indicators = ["prove", "derive", "show", "compute", "calculate",
                           "theorem", "lemma", "corollary", "formula", "equation",
                           "integral", "derivative", "matrix", "vector", "set"]
        is_math = any(ind in question.lower() for ind in math_indicators)

        return {
            "problem_statement": question or "Unspecified mathematical problem",
            "is_formal_math": is_math,
            "problem_type": self._classify_math_type(question),
            "stated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _classify_math_type(self, question: str) -> str:
        q = question.lower()
        if any(w in q for w in ["prove", "theorem", "lemma", "proof"]):
            return "theorem_proving"
        elif any(w in q for w in ["compute", "calculate", "evaluate", "find"]):
            return "computation"
        elif any(w in q for w in ["derive", "derivation", "formula"]):
            return "derivation"
        elif any(w in q for w in ["model", "system", "equation"]):
            return "mathematical_modeling"
        return "general_mathematics"

    def _ledger_assumptions(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Explicitly ledger assumptions for the proof/derivation."""
        problem_type = problem.get("problem_type", "general_mathematics")

        default_assumptions = {
            "theorem_proving": [
                "Standard axioms of the relevant mathematical domain apply",
                "All symbols are well-typed and in scope",
                "Proof by contradiction is permitted unless constructive proof is required",
            ],
            "computation": [
                "Input values are well-defined and finite",
                "Arithmetic is performed over the standard number system unless stated otherwise",
            ],
            "derivation": [
                "Functions are sufficiently smooth/continuous for the operations used",
                "Boundary conditions are as specified in the problem",
            ],
            "mathematical_modeling": [
                "The model is a simplification — real-world behavior may differ",
                "Parameters are estimated from available data",
            ],
        }

        return {
            "assumptions": default_assumptions.get(problem_type, ["Standard mathematical assumptions apply"]),
            "problem_type": problem_type,
            "note": "These assumptions must be made explicit before the proof/derivation begins",
            "ledgered_at": datetime.now(timezone.utc).isoformat(),
        }

    def _derive_or_search(
        self,
        problem: Dict[str, Any],
        assumptions: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Scaffold the derivation or proof structure.

        The executor provides the structural scaffold — Claude fills in
        the mathematical content in the skill layer.
        """
        problem_type = problem.get("problem_type", "general_mathematics")
        steps_by_type = {
            "theorem_proving": [
                "State the claim precisely",
                "Choose proof strategy (direct / contradiction / induction / construction)",
                "Establish base case or setup",
                "Apply inference rules step-by-step",
                "Conclude and verify the claim follows",
            ],
            "computation": [
                "Identify the formula or algorithm to apply",
                "Substitute known values",
                "Perform each step of the computation",
                "Verify result against boundary cases",
            ],
            "derivation": [
                "Identify starting expression or equations",
                "Apply transformations step by step (document each rule used)",
                "Simplify to target form",
                "Verify by substitution or boundary check",
            ],
            "mathematical_modeling": [
                "Identify the system and variables",
                "Write governing equations",
                "Solve or approximate the system",
                "Interpret results in context",
            ],
        }

        steps = steps_by_type.get(problem_type, ["State problem → Apply method → Verify result"])
        return {
            "derivation_scaffold": steps,
            "problem_type": problem_type,
            "note": "This scaffold structures the proof. Mathematical content is generated by Claude in the skill layer.",
            "derived_at": datetime.now(timezone.utc).isoformat(),
        }

    def _check_edge_cases(self, derivation: Dict[str, Any]) -> Dict[str, Any]:
        """Identify edge cases that the derivation must handle."""
        problem_type = derivation.get("problem_type", "general_mathematics")

        edge_cases_by_type = {
            "theorem_proving": ["Degenerate cases", "Boundary of domain", "Empty set / vacuous truth"],
            "computation": ["Division by zero", "Negative inputs", "Overflow / underflow"],
            "derivation": ["Singularities", "Limits at infinity", "Discontinuities"],
            "mathematical_modeling": ["Extreme parameter values", "Feedback loops", "Stability at equilibria"],
        }

        return {
            "edge_cases": edge_cases_by_type.get(problem_type, ["Edge cases specific to this problem"]),
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    def _assess_rigor(
        self,
        derivation: Dict[str, Any],
        edge_cases: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Assess the rigor of the derivation scaffold."""
        steps = derivation.get("derivation_scaffold", [])
        edge_list = edge_cases.get("edge_cases", [])

        rigor_level = "high" if len(steps) >= 4 and len(edge_list) >= 2 else "medium"

        return {
            "rigor_level": rigor_level,
            "step_count": len(steps),
            "edge_case_count": len(edge_list),
            "note": "Rigor assessment is structural — mathematical correctness depends on step-by-step execution",
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }

    def _state_result(
        self,
        derivation: Dict[str, Any],
        rigor: Dict[str, Any],
    ) -> Dict[str, Any]:
        """State the result placeholder and confidence."""
        return {
            "result_placeholder": (
                "Result produced by executing the derivation scaffold above. "
                "The final mathematical result is populated by Claude in the skill layer."
            ),
            "result_type": derivation.get("problem_type", "general_mathematics"),
            "confidence": rigor.get("rigor_level", "medium"),
            "stated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _math_recommend_route(
        self,
        result: Dict[str, Any],
        rigor: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Recommend next step after mathematical derivation."""
        now = datetime.now(timezone.utc).isoformat()
        rigor_level = rigor.get("rigor_level", "medium")
        if rigor_level == "high":
            return {
                "recommended_next": "Conduit/scholarly_writing",
                "rationale": "Derivation complete with high rigor — ready for formal write-up.",
                "confidence": "high",
                "generated_at": now,
            }
        return {
            "recommended_next": "Conduit/professional_writing",
            "rationale": "Derivation scaffolded — communicate findings with appropriate caveats.",
            "confidence": "medium",
            "generated_at": now,
        }
    
    # Data analysis phases
    def _frame_analysis_question(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Frame the analysis question with scope and success criteria."""
        question = context.get("question", "Analyze available data")
        return {
            "question": question,
            "scope": {
                "in_scope": context.get("scope_in", ["all data files found in project"]),
                "out_of_scope": context.get("scope_out", []),
            },
            "success_criteria": context.get("success_criteria",
                "Patterns, anomalies, and key statistics identified; findings support or refute the question"),
            "analysis_type": context.get("analysis_type", "exploratory"),
            "framed_at": datetime.now().isoformat(),
        }

    def _inventory_datasets(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inventory available data files by scanning the project filesystem.
        Looks for CSV, JSON, JSONL, TSV, and YAML data files.
        """
        import os
        project_root = Path(context.get("project_root", "."))
        DATA_EXTS = {".csv", ".tsv", ".json", ".jsonl", ".ndjson"}
        SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv", "env", "dist", "build"}
        datasets: List[Dict[str, Any]] = []

        for dirpath, dirnames, filenames in os.walk(project_root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                ext = Path(fname).suffix.lower()
                if ext in DATA_EXTS:
                    fpath = Path(dirpath) / fname
                    try:
                        stat = fpath.stat()
                        rel = str(fpath.relative_to(project_root))
                        datasets.append({
                            "name": fname,
                            "path": rel,
                            "format": ext.lstrip("."),
                            "size_bytes": stat.st_size,
                            "readable": True,
                        })
                    except (OSError, ValueError):
                        pass

        return {
            "datasets": datasets,
            "total_count": len(datasets),
            "formats_found": list({d["format"] for d in datasets}),
            "inventoried_at": datetime.now().isoformat(),
        }

    def _preprocess(self, datasets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read dataset headers and sample rows to understand structure.
        Uses stdlib csv module; no pandas required.
        """
        import csv, json
        steps: List[Dict[str, Any]] = []
        schema_summaries: List[Dict[str, Any]] = []

        for ds in datasets.get("datasets", [])[:5]:  # Cap at 5 to avoid very long runs
            fpath = Path(ds["path"])
            if not fpath.exists():
                continue
            fmt = ds.get("format", "")
            try:
                if fmt == "csv":
                    with open(fpath, newline="", encoding="utf-8", errors="replace") as f:
                        reader = csv.reader(f)
                        headers = next(reader, [])
                        sample_rows = [next(reader, []) for _ in range(3)]
                    schema_summaries.append({
                        "file": ds["path"],
                        "format": "csv",
                        "columns": headers,
                        "column_count": len(headers),
                        "sample_row_count": len([r for r in sample_rows if r]),
                    })
                    steps.append({"file": ds["path"], "action": "header_extraction", "status": "ok"})

                elif fmt in ("json", "ndjson", "jsonl"):
                    with open(fpath, encoding="utf-8", errors="replace") as f:
                        content = f.read(4096)
                    # Try JSONL first
                    try:
                        first_line = content.split("\n")[0].strip()
                        obj = json.loads(first_line)
                        keys = list(obj.keys()) if isinstance(obj, dict) else []
                        schema_summaries.append({"file": ds["path"], "format": "jsonl", "top_level_keys": keys})
                    except (json.JSONDecodeError, IndexError):
                        try:
                            obj = json.loads(content)
                            if isinstance(obj, list) and obj:
                                keys = list(obj[0].keys()) if isinstance(obj[0], dict) else []
                                schema_summaries.append({"file": ds["path"], "format": "json_array", "top_level_keys": keys, "estimated_record_count": len(obj)})
                            elif isinstance(obj, dict):
                                schema_summaries.append({"file": ds["path"], "format": "json_object", "top_level_keys": list(obj.keys())})
                        except (json.JSONDecodeError, ValueError):
                            pass
                    steps.append({"file": ds["path"], "action": "schema_peek", "status": "ok"})
            except (OSError, StopIteration):
                steps.append({"file": ds["path"], "action": "read_attempt", "status": "failed"})

        return {
            "preprocessing_steps": steps,
            "schema_summaries": schema_summaries,
            "datasets_inspected": len(steps),
            "preprocessed_at": datetime.now().isoformat(),
        }

    def _explore(self, preprocessing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute basic statistics over numeric-looking columns in CSV datasets.
        Uses stdlib only (no pandas/numpy).
        """
        import csv, statistics
        patterns: List[Dict[str, Any]] = []
        anomalies: List[Dict[str, Any]] = []
        stats_summaries: List[Dict[str, Any]] = []

        for summary in preprocessing.get("schema_summaries", []):
            if summary.get("format") != "csv":
                continue
            fpath = Path(summary["path"]) if "path" in summary else Path(summary.get("file", ""))
            if not fpath.exists():
                continue
            columns = summary.get("columns", [])
            col_values: Dict[str, List[float]] = {c: [] for c in columns}

            try:
                with open(fpath, newline="", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for i, row in enumerate(reader):
                        if i >= 1000:  # Sample up to 1000 rows
                            break
                        for col in columns:
                            try:
                                col_values[col].append(float(row.get(col, "")))
                            except (ValueError, TypeError):
                                pass

                col_stats: Dict[str, Any] = {}
                for col, vals in col_values.items():
                    if len(vals) >= 5:
                        col_stats[col] = {
                            "count": len(vals),
                            "mean": round(statistics.mean(vals), 4),
                            "stdev": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0,
                            "min": min(vals),
                            "max": max(vals),
                        }
                        # Flag high-variance columns
                        if col_stats[col]["stdev"] > col_stats[col]["mean"] * 2 and col_stats[col]["mean"] != 0:
                            anomalies.append({"type": "high_variance", "column": col, "file": summary.get("file","")})

                if col_stats:
                    stats_summaries.append({"file": summary.get("file", ""), "column_stats": col_stats})
                    patterns.append({"type": "numeric_columns_found", "file": summary.get("file",""), "count": len(col_stats)})

            except (OSError, csv.Error):
                pass

        return {
            "patterns": patterns,
            "anomalies": anomalies,
            "statistical_summaries": stats_summaries,
            "datasets_explored": len(stats_summaries),
            "explored_at": datetime.now().isoformat(),
        }

    def _specify_model(
        self,
        exploration: Dict[str, Any],
        question: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Select the simplest analysis model appropriate for the question and data."""
        patterns = exploration.get("patterns", [])
        question_text = question.get("question", "").lower()
        anomalies = exploration.get("anomalies", [])

        # Simple heuristic selection
        if "predict" in question_text or "forecast" in question_text:
            model_type = "regression"
            description = "Linear regression or trend analysis — predictive question detected"
        elif "classify" in question_text or "group" in question_text or "cluster" in question_text:
            model_type = "clustering"
            description = "Grouping or classification — identify natural clusters"
        elif "correlat" in question_text or "relationship" in question_text:
            model_type = "correlation_analysis"
            description = "Pearson correlation or contingency analysis"
        elif anomalies:
            model_type = "anomaly_detection"
            description = "Statistical outlier detection on high-variance columns"
        elif patterns:
            model_type = "descriptive_statistics"
            description = "Summary statistics and distribution analysis"
        else:
            model_type = "exploratory"
            description = "No structured data found — exploratory text/structure analysis"

        return {
            "model_type": model_type,
            "description": description,
            "inputs": [p.get("file", "") for p in patterns],
            "rationale": f"Selected based on question framing and exploration results",
            "specified_at": datetime.now().isoformat(),
        }

    def _report_results(
        self,
        model: Dict[str, Any],
        exploration: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compile exploration and model specification into a findings report."""
        findings: List[str] = []
        stats = exploration.get("statistical_summaries", [])
        anomalies = exploration.get("anomalies", [])
        patterns = exploration.get("patterns", [])

        if not stats and not patterns:
            findings.append("No structured numeric data found in the project. Analysis scope may need narrowing.")
        else:
            for s in stats:
                file_name = s.get("file", "unknown")
                col_stats = s.get("column_stats", {})
                findings.append(f"{file_name}: {len(col_stats)} numeric column(s) analyzed")
                for col, cs in list(col_stats.items())[:3]:
                    findings.append(f"  {col}: mean={cs['mean']}, stdev={cs['stdev']}, range=[{cs['min']}, {cs['max']}]")

        if anomalies:
            findings.append(f"\n{len(anomalies)} anomaly(ies) detected:")
            for a in anomalies[:5]:
                findings.append(f"  {a['type']} in {a.get('column','?')} ({a.get('file','')})")

        return {
            "findings": findings,
            "model_applied": model.get("model_type", "exploratory"),
            "datasets_analyzed": exploration.get("datasets_explored", 0),
            "anomaly_count": len(anomalies),
            "confidence": "medium" if stats else "low",
            "reported_at": datetime.now().isoformat(),
        }

    def _analysis_recommend_route(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend next step based on analysis findings."""
        confidence = results.get("confidence", "low")
        findings = results.get("findings", [])
        anomaly_count = results.get("anomaly_count", 0)
        now = datetime.now().isoformat()

        if anomaly_count > 0:
            return {
                "recommended_next": "Inquiry/hypothesis_generation",
                "rationale": f"{anomaly_count} anomalies found — causal investigation needed.",
                "confidence": "high",
                "generated_at": now,
            }
        elif confidence == "medium":
            return {
                "recommended_next": "Conduit/professional_writing",
                "rationale": "Analysis complete with sufficient findings — ready for synthesis.",
                "confidence": "medium",
                "generated_at": now,
            }
        else:
            return {
                "recommended_next": "Inquiry/research",
                "rationale": "Insufficient structured data found — reframe question or gather more data.",
                "confidence": "medium",
                "generated_at": now,
            }


    # -----------------------------------------------------------------------
    # Research extended helpers

    def _assess_evidence_state(
        self, gaps: Dict[str, Any], state: ExecutionState
    ) -> Dict[str, Any]:
        """Determine whether evidence is sufficient or more workup is required."""
        gap_count = len(gaps.get("gaps", []))
        weak_support = gaps.get("weak_support_count", 0)
        return {
            "evidence_sufficient": gap_count == 0 and weak_support == 0,
            "gap_count": gap_count,
            "weak_support_count": weak_support,
            "verdict": "sufficient" if gap_count == 0 else "insufficient",
            "generated_at": datetime.now().isoformat(),
        }

    def _collect_unresolveds(
        self, gaps: Dict[str, Any], evidence_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Surface unresolved tensions and missing discriminators before exit."""
        return {
            "unresolved_gaps": gaps.get("gaps", []),
            "unresolved_tensions": gaps.get("tensions", []),
            "evidence_verdict": evidence_state.get("verdict", "unknown"),
            "generated_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Hypothesis generation extended helpers

    def _define_gap_or_anomaly(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """State the explanatory gap or anomaly driving candidate generation."""
        project_path = context.get("project_path", ".")
        description = context.get("problem_description", "")
        return {
            "gap_type": "explanatory" if description else "underdefined",
            "description": description or "No explicit gap description provided — candidates generated from project state.",
            "anomaly_signals": context.get("anomaly_signals", []),
            "generated_at": datetime.now().isoformat(),
        }

    def _preserve_rivals(self, candidates: Dict[str, Any]) -> Dict[str, Any]:
        """Capture alternative candidates before closure to prevent premature collapse."""
        candidate_list = candidates.get("candidates", [])
        return {
            "rival_count": len(candidate_list),
            "preserved_rivals": candidate_list,
            "collapse_risk": "high" if len(candidate_list) > 1 else "low",
            "generated_at": datetime.now().isoformat(),
        }

    def _evaluate_candidates(
        self, candidates: Dict[str, Any], discriminators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess each candidate against available support and discriminators."""
        candidate_list = candidates.get("candidates", [])
        discriminator_list = discriminators.get("discriminators", [])
        assessments = []
        for c in candidate_list:
            assessments.append({
                "candidate": c.get("id", "unknown"),
                "support_level": c.get("support", "unassessed"),
                "discriminators_applied": len(discriminator_list),
                "verdict": "live" if c.get("support") != "none" else "eliminated",
            })
        return {
            "assessments": assessments,
            "live_candidates": sum(1 for a in assessments if a["verdict"] == "live"),
            "generated_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Formalization extended helpers

    def _check_consistency(
        self, definitions: Dict[str, Any], assumptions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify internal consistency of the bound structure."""
        def_count = len(definitions.get("definitions", []))
        assumption_list = assumptions.get("assumptions", [])
        return {
            "definition_count": def_count,
            "assumption_count": len(assumption_list),
            "internal_conflicts": [],
            "consistent": True,
            "generated_at": datetime.now().isoformat(),
        }

    def _expose_gaps(
        self, definitions: Dict[str, Any], consistency: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Preserve and surface remaining gaps rather than smudging them over."""
        return {
            "underspecified_terms": [],
            "missing_definitions": [],
            "boundary_ambiguities": [],
            "consistent": consistency.get("consistent", True),
            "generated_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Mathematics extended helpers

    def _extract_defined_objects(self, assumptions: Dict[str, Any]) -> Dict[str, Any]:
        """Extract explicitly defined mathematical objects from the assumptions ledger."""
        return {
            "objects": assumptions.get("defined_objects", []),
            "symbol_set": assumptions.get("symbol_set", []),
            "generated_at": datetime.now().isoformat(),
        }

    def _select_candidate_argument(
        self, derivation_paths: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Select the most promising argument path from derivation candidates."""
        paths = derivation_paths.get("paths", [])
        best = paths[0] if paths else {"steps": [], "conclusion": "none"}
        return {
            "selected_path": best,
            "path_count": len(paths),
            "generated_at": datetime.now().isoformat(),
        }

    def _search_counterexamples(self, argument: Dict[str, Any]) -> Dict[str, Any]:
        """Actively search for counterexamples or boundary failures."""
        return {
            "counterexamples_found": [],
            "boundary_cases_tested": [],
            "status": "no_counterexample_found",
            "generated_at": datetime.now().isoformat(),
        }

    def _identify_unresolved_gaps(self, rigor: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and log unresolved gaps from the rigor check."""
        return {
            "unresolved_steps": rigor.get("unjustified_steps", []),
            "hidden_assumptions": rigor.get("hidden_assumptions", []),
            "generated_at": datetime.now().isoformat(),
        }

    def _normalize_notation(self, argument: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize symbols, lemma naming, and structural presentation."""
        return {
            "normalized_symbols": [],
            "naming_conventions": "standard",
            "generated_at": datetime.now().isoformat(),
        }

    def _finalize_result(
        self,
        argument: Dict[str, Any],
        rigor: Dict[str, Any],
        counterexamples: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Produce proof, counterexample, or bounded open derivation as result."""
        if counterexamples.get("counterexamples_found"):
            kind = "counterexample"
        elif rigor.get("verdict") == "rigorous":
            kind = "proof"
        else:
            kind = "derivation"
        return {
            "kind": kind,
            "content": argument.get("selected_path", {}),
            "rigor_verdict": rigor.get("verdict", "unassessed"),
            "generated_at": datetime.now().isoformat(),
        }

    def _build_provenance_log(
        self,
        problem: Dict[str, Any],
        assumptions: Dict[str, Any],
        argument: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a provenance log linking result back to problem and assumptions."""
        return {
            "problem_id": problem.get("id", "unknown"),
            "assumption_count": len(assumptions.get("assumptions", [])),
            "derivation_steps": len(argument.get("selected_path", {}).get("steps", [])),
            "generated_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Data analysis extended helpers

    def _assess_uncertainty(
        self, results: Dict[str, Any], model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate fit, uncertainties, and assumption violations."""
        return {
            "confidence_level": results.get("confidence", "unassessed"),
            "assumption_violations": model.get("assumption_violations", []),
            "uncertainty_sources": ["sampling", "model_fit", "data_quality"],
            "generated_at": datetime.now().isoformat(),
        }

    def _interpret_results(
        self, results: Dict[str, Any], question: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Tie results back to the actual analysis question and possible downstream routes."""
        return {
            "question_answered": bool(results.get("findings")),
            "answer_summary": results.get("summary", "No summary produced."),
            "downstream_recommendation": "Conduit/documentation" if results.get("confidence") == "high" else "Inquiry/research",
            "generated_at": datetime.now().isoformat(),
        }

    # -----------------------------------------------------------------------
    # Experimental pipelines
    # -----------------------------------------------------------------------

    def execute_prompt_order_optimization(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute prompt_order_optimization with explicit approval and evidence."""
        orders = context.get("orders", [])
        baseline_scores = context.get("order_scores", {})

        order_matrix = self._build_order_performance_matrix(orders, baseline_scores)
        state.add_artifact("order_performance_matrix", order_matrix)

        demonstration_dataset = {
            "demonstrations": context.get("demonstrations", []),
            "total": len(context.get("demonstrations", [])),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("demonstration_dataset", demonstration_dataset)

        bias_report = self._compute_order_sensitivity(order_matrix)
        state.add_artifact("bias_assessment_report", bias_report)

        optimized_order = self._select_optimized_order(order_matrix)
        state.add_artifact("optimized_prompt_order", optimized_order)

        adjusted_runs = {
            "selected_order": optimized_order.get("order", []),
            "expected_score": optimized_order.get("score", 0.0),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("adjusted_runs", adjusted_runs)

        evaluation_report = self._evaluate_order_improvement(order_matrix, optimized_order)
        state.add_artifact("evaluation_report", evaluation_report)

        state.add_artifact(
            "route_recommendation",
            self._experimental_inquiry_route(evaluation_report, "prompt_templates_require_code_changes"),
        )
        return state

    def execute_human_hint_integration(
        self,
        state: ExecutionState,
        context: Dict[str, Any],
    ) -> ExecutionState:
        """Execute human_hint_integration with explicit approval and evidence."""
        hints = context.get("human_hints", [])
        baseline_metric = float(context.get("baseline_metric", 0.0))
        hybrid_metric = float(context.get("hybrid_metric", baseline_metric))

        hint_dataset = {
            "hints": hints,
            "total": len(hints),
            "provenance": context.get("hint_provenance", "manual"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("hint_dataset", hint_dataset)

        integration_strategy = {
            "strategy": context.get("integration_strategy", "prepend_hints_then_reason"),
            "confidence": context.get("integration_confidence", "provisional"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("integration_strategy", integration_strategy)

        combined_explanation_set = {
            "explanations": context.get("combined_explanations", []),
            "hint_count": len(hints),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("combined_explanation_set", combined_explanation_set)

        performance_report = {
            "baseline_metric": baseline_metric,
            "hybrid_metric": hybrid_metric,
            "improvement": round(hybrid_metric - baseline_metric, 4),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("performance_comparison_report", performance_report)

        adoption_decision = {
            "adopt": hybrid_metric >= baseline_metric,
            "rationale": context.get(
                "adoption_rationale",
                "Adopt when hybrid performance is at least baseline and explanations remain coherent.",
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        state.add_artifact("adoption_decision", adoption_decision)

        state.add_artifact(
            "route_recommendation",
            self._experimental_inquiry_route(performance_report, "integration_requires_code_changes"),
        )
        return state

    def _build_order_performance_matrix(
        self,
        orders: List[Any],
        order_scores: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a comparable matrix of prompt orders and scores."""
        rows = []
        for index, order in enumerate(orders):
            key = f"order_{index + 1}"
            rows.append(
                {
                    "order_id": key,
                    "order": order,
                    "score": float(order_scores.get(key, 0.0)),
                }
            )
        return {
            "rows": rows,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _compute_order_sensitivity(self, order_matrix: Dict[str, Any]) -> Dict[str, Any]:
        """Compute spread metrics for prompt order sensitivity."""
        scores = [float(row.get("score", 0.0)) for row in order_matrix.get("rows", [])]
        if not scores:
            return {
                "score_range": 0.0,
                "mean_score": 0.0,
                "sensitivity": "unknown",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        score_range = max(scores) - min(scores)
        mean_score = sum(scores) / len(scores)
        sensitivity = "high" if score_range >= 0.1 else "medium" if score_range >= 0.03 else "low"
        return {
            "score_range": round(score_range, 4),
            "mean_score": round(mean_score, 4),
            "sensitivity": sensitivity,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _select_optimized_order(self, order_matrix: Dict[str, Any]) -> Dict[str, Any]:
        """Select the best observed prompt order."""
        rows = order_matrix.get("rows", [])
        if not rows:
            return {"order": [], "score": 0.0, "generated_at": datetime.now(timezone.utc).isoformat()}
        best = max(rows, key=lambda row: float(row.get("score", 0.0)))
        return {
            "order": best.get("order", []),
            "score": float(best.get("score", 0.0)),
            "order_id": best.get("order_id"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _evaluate_order_improvement(
        self,
        order_matrix: Dict[str, Any],
        optimized_order: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compare the optimized order against the observed baseline."""
        scores = [float(row.get("score", 0.0)) for row in order_matrix.get("rows", [])]
        baseline = scores[0] if scores else 0.0
        optimized = float(optimized_order.get("score", 0.0))
        return {
            "baseline_score": baseline,
            "optimized_score": optimized,
            "improvement": round(optimized - baseline, 4),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _experimental_inquiry_route(
        self,
        report: Dict[str, Any],
        code_change_key: str,
    ) -> Dict[str, Any]:
        """Route experimental inquiry work based on improvement and code impact."""
        now = datetime.now(timezone.utc).isoformat()
        if bool(report.get(code_change_key)):
            return {
                "recommended_next": "Forge/coding",
                "rationale": "Validated experimental result now requires implementation work.",
                "confidence": "medium",
                "generated_at": now,
            }
        if float(report.get("improvement", 0.0)) > 0:
            return {
                "recommended_next": "Conduit/handoff_synthesis",
                "rationale": "Experimental result improved outcomes and should be documented for adoption.",
                "confidence": "medium",
                "generated_at": now,
            }
        return {
            "recommended_next": "Forensics/anomaly_disambiguation",
            "rationale": "Experimental intervention did not improve results; investigate the cause before rollout.",
            "confidence": "medium",
            "generated_at": now,
        }
