from dataclasses import dataclass, field
from typing import Dict, List, Any
from uuid import uuid4


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass
class AcademicTask:
    task_type: str
    requester_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "created"
    result: Dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False
    approved_by: str = ""
    id: str = field(default_factory=lambda: uid("academic_task"))


@dataclass
class LearningPlan:
    student_id: str
    goals: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weak_topics: List[str] = field(default_factory=list)
    activities: List[str] = field(default_factory=list)
    status: str = "draft"
    id: str = field(default_factory=lambda: uid("learning_plan"))


@dataclass
class AcademicAgentResult:
    task_id: str
    agent: str
    action: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
