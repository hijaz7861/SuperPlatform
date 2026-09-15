
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SourceReference:
    source_id: str
    source_type: str
    title: str
    locator: str = ""
    author: str = ""
    edition: str = ""
    language: str = ""
    url: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceItem:
    evidence_id: str
    source: SourceReference
    excerpt: str = ""
    relevance: float = 0.0
    verified: bool = False
    verification_method: str = ""
    notes: str = ""

    def __post_init__(self):
        if not 0.0 <= self.relevance <= 1.0:
            raise ValueError("Relevance must be between 0 and 1")


@dataclass
class ResearchQuestion:
    question_id: str
    question: str
    category: str = "general"
    requested_by: str = "user"
    created_at: str = field(default_factory=utc_now)


@dataclass
class GuidanceResult:
    result_id: str
    question_id: str
    status: str
    answer: str
    evidence: List[EvidenceItem] = field(default_factory=list)
    confidence: float = 0.0
    requires_human_review: bool = True
    disagreement: bool = False
    notes: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")
