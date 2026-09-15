
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class TeacherRequest:
    teacher_id: str
    request: str
    subject: str = ""
    class_name: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LessonPlan:
    title: str
    subject: str
    class_name: str
    objectives: List[str] = field(default_factory=list)
    activities: List[str] = field(default_factory=list)
    assessment_ideas: List[str] = field(default_factory=list)
    status: str = "draft"


@dataclass
class TeacherRecommendation:
    category: str
    recommendation: str
    priority: str = "normal"
    evidence: List[str] = field(default_factory=list)


@dataclass
class TeacherAssistantResult:
    teacher_id: str
    intent: str
    output: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    requires_approval: bool = False
