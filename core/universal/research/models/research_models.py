from dataclasses import dataclass, field
from typing import List


@dataclass
class ResearchQuestion:
    question_id: str
    question: str
    status: str = "OPEN"


@dataclass
class ResearchFinding:
    source: str
    claim: str
    confidence: float
    verified: bool = False


@dataclass
class ResearchResult:
    question_id: str
    findings: List[ResearchFinding] = field(default_factory=list)
    status: str = "IN_PROGRESS"
