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
                self.escalation_rules = yaml.safe_load(f)
        
        # Load commitment rules
        commit_path = lever_dir / "commitment_rules.yaml"
        if commit_path.exists():
            with open(commit_path, 'r') as f:
                self.commitment_rules = yaml.safe_load(f)
    
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
        
        # Apply evaluator logic
        eval_type = evaluator.get("type", "generic")
        
        if eval_type == "trust_check":
            findings = self._evaluate_trust(context)
        elif eval_type == "contradiction_check":
            findings = self._evaluate_contradiction(context)
        elif eval_type == "support_check":
            findings = self._evaluate_support(context)
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
    
    def _evaluate_generic(
        self,
        evaluator: Dict[str, Any],
        context: Dict[str, Any],
    ) -> List[str]:
        """Generic evaluation when no specific type matches."""
        findings = []
        
        criteria = evaluator.get("criteria", [])
        for criterion in criteria:
            if isinstance(criterion, str):
                if criterion not in context:
                    findings.append(f"Criterion not met: {criterion}")
        
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
