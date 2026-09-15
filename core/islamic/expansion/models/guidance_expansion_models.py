
from dataclasses import dataclass, field
from typing import List


@dataclass
class GuidanceCase:
    case_id: str
    topic: str
    evidence_ids: List[str] = field(default_factory=list)
    status: str = "REVIEW_REQUIRED"
    human_review_required: bool = True
