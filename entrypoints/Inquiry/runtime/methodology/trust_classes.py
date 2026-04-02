"""Trust classes for forensic state classification.

Trust classes are used by Forensics to mark surfaces, artifacts, and claims.
They should be applied to observed state, not to preferred narratives.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TrustClass(str, Enum):
    CANONICAL = "canonical"
    VERIFIED = "verified"
    PLAUSIBLE = "plausible"
    STALE = "stale"
    CONFLICTING = "conflicting"
    ORPHANED = "orphaned"
    ASPIRATIONAL = "aspirational"
    UNKNOWN = "unknown"
    CONTAMINATED = "contaminated"


class ConsequenceClass(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class TrustAssessment:
    subject_id: str
    trust_class: TrustClass
    basis: str
    source: Optional[str] = None
    consequence_class: ConsequenceClass = ConsequenceClass.MODERATE
    stale_signal: bool = False
    conflicting_signal: bool = False
    notes: str = ""


TRUST_CLASS_GUIDANCE = {
    TrustClass.CANONICAL: "Primary source of truth; load-bearing and explicitly preferred over alternatives.",
    TrustClass.VERIFIED: "Observed or checked against trustworthy state and usable for downstream work.",
    TrustClass.PLAUSIBLE: "Reasonable but not yet established strongly enough to anchor high-consequence action.",
    TrustClass.STALE: "May once have been true, but temporal drift risk is meaningful.",
    TrustClass.CONFLICTING: "Disagrees with another relevant surface or observation in a consequential way.",
    TrustClass.ORPHANED: "Exists without reliable provenance or clear relation to current canonical state.",
    TrustClass.ASPIRATIONAL: "Describes intended or documented state, not necessarily observed state.",
    TrustClass.UNKNOWN: "Insufficient evidence for classification.",
    TrustClass.CONTAMINATED: "State is materially compromised by drift, ambiguity, or mixture of inconsistent sources.",
}


def requires_forensics_reset(assessment: TrustAssessment) -> bool:
    return assessment.trust_class in {
        TrustClass.CONFLICTING,
        TrustClass.CONTAMINATED,
    } and assessment.consequence_class in {
        ConsequenceClass.HIGH,
        ConsequenceClass.CRITICAL,
    }


__all__ = [
    "TrustClass",
    "ConsequenceClass",
    "TrustAssessment",
    "TRUST_CLASS_GUIDANCE",
    "requires_forensics_reset",
]
