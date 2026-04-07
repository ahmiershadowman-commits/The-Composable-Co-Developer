"""
Lever escalation for evaluation and commitment.

Lever handles bounded evaluation, escalation decisions,
commitment rules, and reopen behaviors.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EvaluationResult:
    """Result from Lever evaluation."""
    evaluator_id: str
    success: bool
    findings: List[str]
    recommendation: Optional[str]
    commitment_level: Optional[str]
    reopen_conditions: List[str]


class LeverEscalation:
    """
    Handles escalation to Lever for bounded evaluation.
    
    Dispatches evaluators and returns structured results.
    """
    
    def __init__(self):
        self.evaluators: Dict[str, Dict[str, Any]] = {}
        self.escalation_rules: Dict[str, Any] = {}
        self.commitment_rules: Dict[str, Any] = {}
        self._load_specs()
    
    def _load_specs(self) -> None:
        """Load Lever specification files."""
        import yaml
        
        lever_dir = Path(__file__).parent.parent.parent / "shared" / "Lever"
        
        # Load evaluator registry
        eval_path = lever_dir / "evaluator_registry.yaml"
        if eval_path.exists():
            with open(eval_path, 'r') as f:
                registry = yaml.safe_load(f)
                for eval_id, spec in registry.get("evaluators", {}).items():
                    self.evaluators[eval_id] = spec
        
        # Load escalation rules
        esc_path = lever_dir / "escalation_rules.yaml"
        if esc_path.exists():
            with open(esc_path, 'r') as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    self.escalation_rules = loaded
                else:
                    import warnings
                    warnings.warn(
                        f"escalation_rules.yaml at {esc_path} did not parse to a dict; "
                        "escalation rules will be empty."
                    )
        else:
            import warnings
            warnings.warn(
                f"Lever escalation_rules.yaml not found at {esc_path}; "
                "escalate() will use default behaviour."
            )

        # Load commitment rules
        commit_path = lever_dir / "commitment_rules.yaml"
        if commit_path.exists():
            with open(commit_path, 'r') as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    self.commitment_rules = loaded
                else:
                    import warnings
                    warnings.warn(
                        f"commitment_rules.yaml at {commit_path} did not parse to a dict; "
                        "commitment rules will be empty."
                    )
        else:
            import warnings
            warnings.warn(
                f"Lever commitment_rules.yaml not found at {commit_path}; "
                "commit() will use default behaviour."
            )
    
    def evaluate(
        self,
        evaluator_id: str,
        context: Dict[str, Any],
    ) -> EvaluationResult:
        """
        Dispatch an evaluator and return structured result.
        """
        if evaluator_id not in self.evaluators:
            return EvaluationResult(
                evaluator_id=evaluator_id,
                success=False,
                findings=[f"Unknown evaluator: {evaluator_id}"],
                recommendation=None,
                commitment_level=None,
                reopen_conditions=[],
            )
        
        evaluator = self.evaluators[evaluator_id]
        findings = []

        # Dispatch by evaluator ID (specs use use_when/returns, not a type key)
        _dispatch = {
            "trust_evaluator": self._evaluate_trust,
            "contradiction_evaluator": self._evaluate_contradiction,
            "support_evaluator": self._evaluate_support,
            "discriminator_evaluator": self._evaluate_discriminator,
            "frame_evaluator": self._evaluate_frame,
            "artifact_shape_evaluator": self._evaluate_artifact_shape,
        }
        handler = _dispatch.get(evaluator_id)
        if handler is not None:
            findings = handler(context)
        else:
            findings = self._evaluate_generic(evaluator, context)
        
        # Determine recommendation
        recommendation = self._get_recommendation(evaluator_id, findings, context)
        commitment_level = self._get_commitment_level(findings)
        reopen_conditions = evaluator.get("reopen_conditions", [])
        
        return EvaluationResult(
            evaluator_id=evaluator_id,
            success=True,
            findings=findings,
            recommendation=recommendation,
            commitment_level=commitment_level,
            reopen_conditions=reopen_conditions,
        )
    
    def _evaluate_trust(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate trust in the state surface."""
        findings = []
        
        # Check for canonical sources
        if not context.get("canonical_sources_identified"):
            findings.append("No canonical sources identified")
        
        # Check for discrepancies
        discrepancy_count = context.get("discrepancy_count", 0)
        if discrepancy_count > 0:
            findings.append(f"{discrepancy_count} discrepancies detected")
        
        # Check for coherence
        if not context.get("coherence_restored", True):
            findings.append("Coherence not yet restored")
        
        return findings
    
    def _evaluate_contradiction(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate for contradictions in claims."""
        findings = []
        
        claims = context.get("claims", [])
        if len(claims) > 1:
            # Check for conflicting claims
            findings.append(f"{len(claims)} claims present - checking for contradictions")
        
        return findings
    
    def _evaluate_support(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate evidential support for claims."""
        findings = []
        
        evidence = context.get("evidence", [])
        gaps = context.get("evidence_gaps", [])
        
        if len(evidence) == 0:
            findings.append("No evidence provided")
        
        if len(gaps) > 0:
            findings.append(f"{len(gaps)} evidence gaps identified")
        
        return findings
    
    def _evaluate_discriminator(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate branch sprawl and candidate discrimination."""
        findings = []
        candidates = context.get("candidates", [])
        discriminators = context.get("discriminators", [])

        if len(candidates) > 3 and not discriminators:
            findings.append(f"{len(candidates)} candidates present with no discriminator set")

        if context.get("branch_sprawl"):
            findings.append("Branch sprawl detected — candidates competing without evidence ranking")

        if not context.get("candidate_ranking_basis"):
            findings.append("No candidate ranking basis provided")

        return findings

    def _evaluate_frame(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate whether the problem framing is correct."""
        findings = []

        if context.get("wrong_question_risk"):
            findings.append("Wrong-question risk flagged — frame may be misaligned")

        failure_count = context.get("repeated_local_failure_count", 0)
        if failure_count >= 2:
            findings.append(
                f"{failure_count} repeated local failures with stable surface — "
                "frame error may be masking root cause"
            )

        if context.get("route_masking_frame_error"):
            findings.append("Route choice may be masking a frame error — reframe recommended")

        return findings

    def _evaluate_artifact_shape(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate artifact structure and metadata coherence."""
        findings = []

        violations = context.get("shape_violations", [])
        if violations:
            findings.extend(f"Shape violation: {v}" for v in violations)

        if context.get("metadata_incoherence"):
            findings.append("Metadata incoherence detected across artifacts")

        if context.get("artifact_sprawl"):
            findings.append("Artifact sprawl detected — handoff risk present")

        if not context.get("artifact_names_canonical"):
            findings.append("Artifact names do not match spec-canonical names")

        return findings

    def _evaluate_generic(
        self,
        evaluator: Dict[str, Any],
        context: Dict[str, Any],
    ) -> List[str]:
        """Generic evaluation for unrecognised evaluator IDs.

        Checks use_when conditions against context keys so that any future
        evaluator added to the registry gets at least basic signal even before
        it has a dedicated handler.
        """
        findings = []

        # use_when lists the context conditions that should trigger this evaluator
        use_when = evaluator.get("use_when", [])
        for condition in use_when:
            if isinstance(condition, str) and context.get(condition):
                findings.append(f"Condition active: {condition}")

        # Fallback: surface expected returns that are missing from context
        returns = evaluator.get("returns", [])
        for expected_key in returns:
            if isinstance(expected_key, str) and expected_key not in context:
                findings.append(f"Expected return missing from context: {expected_key}")

        return findings
    
    def _get_recommendation(
        self,
        evaluator_id: str,
        findings: List[str],
        context: Dict[str, Any],
    ) -> Optional[str]:
        """Get recommendation based on evaluation."""
        # Check escalation rules
        rules = self.escalation_rules.get("rules", [])
        for rule in rules:
            if rule.get("evaluator") == evaluator_id:
                conditions = rule.get("conditions", [])
                if all(c in findings for c in conditions):
                    return rule.get("action")
        
        # Default recommendation
        if len(findings) > 0:
            return "authority:Trace"
        
        return "continue"
    
    def _get_commitment_level(self, findings: List[str]) -> Optional[str]:
        """Determine commitment level from findings."""
        if len(findings) == 0:
            return "high"
        elif len(findings) <= 2:
            return "medium"
        else:
            return "low"
    
    def escalate(
        self,
        from_authority: str,
        reason: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Handle escalation from another authority.
        
        Returns escalation decision.
        """
        # Log escalation
        escalation_record = {
            "from": from_authority,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "context_summary": {k: str(v)[:100] for k, v in context.items()},
        }
        
        # Check escalation rules
        rules = self.escalation_rules.get("escalation_paths", {})
        next_step = rules.get(from_authority, "evaluate_and_return")
        
        return {
            "escalation_record": escalation_record,
            "next_step": next_step,
            "requires_evaluation": True,
        }
    
    def commit(
        self,
        decision: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Record a commitment.
        
        Returns commitment record with reopen conditions.
        """
        # Check commitment rules
        rules = self.commitment_rules.get("rules", [])
        reopen_conditions = []
        
        for rule in rules:
            if rule.get("decision_type") == decision:
                reopen_conditions = rule.get("reopen_conditions", [])
                break
        
        return {
            "decision": decision,
            "committed_at": datetime.now().isoformat(),
            "reopen_conditions": reopen_conditions,
            "context_preserved": True,
        }
