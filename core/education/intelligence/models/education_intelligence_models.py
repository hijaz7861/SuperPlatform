from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class TopicPerformance:
    student_id: str
    topic: str
    score: float
    attempts: int = 0
    mastery: float = 0.0


@dataclass
class LearningPlan:
    student_id: str
    goals: List[str] = field(default_factory=list)
    weak_topics: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    status: str = "draft"


@dataclass
class RemediationTask:
    student_id: str
    topic: str
    action: str
    priority: str = "normal"
    status: str = "recommended"


@dataclass
class IntelligenceResult:
    action: str
    student_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    requires_review: bool = False


@dataclass
class AcademicWorkflowState:
    workflow_id: str
    student_id: str
    stages: List[str] = field(default_factory=list)
    current_stage: str = "created"
    status: str = "active"
