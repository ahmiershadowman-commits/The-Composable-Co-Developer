"""Experimental pipeline approval policy helpers."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class ExperimentalApprovalError(ValueError):
    """Raised when an experimental approval payload is incomplete."""


@dataclass
class ExperimentalApproval:
    """Structured approval record for running an experimental pipeline."""

    ticket: str
    rationale: str
    rollback_plan: str
    empirical_evidence: List[str] = field(default_factory=list)
    approved_by: str = "local-operator"

    @classmethod
    def from_context(cls, payload: Optional[Dict[str, Any]]) -> "ExperimentalApproval":
        """Construct and validate an approval payload from pipeline context."""
        if not payload:
            raise ExperimentalApprovalError(
                "Experimental pipelines require an 'experimental_approval' payload."
            )

        approval = cls(
            ticket=str(payload.get("ticket", "")).strip(),
            rationale=str(payload.get("rationale", "")).strip(),
            rollback_plan=str(payload.get("rollback_plan", "")).strip(),
            empirical_evidence=[
                str(item).strip()
                for item in payload.get("empirical_evidence", [])
                if str(item).strip()
            ],
            approved_by=str(payload.get("approved_by", "local-operator")).strip(),
        )
        approval.validate()
        return approval

    def validate(self) -> None:
        """Validate that the approval contains the minimum safety fields."""
        missing = []
        if not self.ticket:
            missing.append("ticket")
        if not self.rationale:
            missing.append("rationale")
        if not self.rollback_plan:
            missing.append("rollback_plan")
        if not self.empirical_evidence:
            missing.append("empirical_evidence")

        if missing:
            raise ExperimentalApprovalError(
                "Experimental approval is incomplete: missing "
                + ", ".join(sorted(missing))
            )

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable representation."""
        return {
            "ticket": self.ticket,
            "rationale": self.rationale,
            "rollback_plan": self.rollback_plan,
            "empirical_evidence": self.empirical_evidence,
            "approved_by": self.approved_by,
        }
