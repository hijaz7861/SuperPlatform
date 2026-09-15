from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class StudentRequest:
    student_id: str
    action: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StudentLearningPlan:
    student_id: str
    goals: List[str]
    topics: List[str]
    priorities: List[str]
    status: str = "DRAFT"


@dataclass
class StudentRecommendation:
    student_id: str
    topic: str
    recommendation: str
    priority: str
    confidence: float


@dataclass
class StudentAssistantResult:
    student_id: str
    action: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
