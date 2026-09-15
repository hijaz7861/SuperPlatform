
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class ContentUnit:
    id: str
    title: str
    text: str
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Topic:
    name: str
    evidence: List[str] = field(default_factory=list)


@dataclass
class LearningObjective:
    objective: str
    topic: str
    cognitive_level: str = "understand"


@dataclass
class GeneratedQuestion:
    question: str
    topic: str
    difficulty: str = "medium"
    cognitive_level: str = "understand"
    answer: str = ""
    source_evidence: List[str] = field(default_factory=list)
    verified: bool = False


@dataclass
class ContentAnalysis:
    content_id: str
    topics: List[Topic] = field(default_factory=list)
    objectives: List[LearningObjective] = field(default_factory=list)
    questions: List[GeneratedQuestion] = field(default_factory=list)
    confidence: float = 0.0
    requires_review: bool = False
