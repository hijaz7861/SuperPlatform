from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4

def uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"

@dataclass
class Teacher:
    name: str
    subjects: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    role: str = "teacher"
    id: str = field(default_factory=lambda: uid("teacher"))

@dataclass
class Student:
    name: str
    class_name: str
    subjects: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: uid("student"))

@dataclass
class AttendanceRecord:
    teacher_id: str
    date: str
    status: str
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    id: str = field(default_factory=lambda: uid("attendance"))

@dataclass
class BookDocument:
    title: str
    text: str
    source: str = "local"
    id: str = field(default_factory=lambda: uid("book"))

@dataclass
class Topic:
    book_id: str
    title: str
    chapter: str = ""
    keywords: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: uid("topic"))

@dataclass
class Question:
    text: str
    question_type: str
    difficulty: str
    subject: str
    topic: str
    marks: int = 1
    learning_objective: str = ""
    id: str = field(default_factory=lambda: uid("question"))

@dataclass
class Exam:
    title: str
    subject: str
    class_name: str
    duration_minutes: int
    total_marks: int
    question_ids: List[str] = field(default_factory=list)
    status: str = "draft"
    approved_by: Optional[str] = None
    id: str = field(default_factory=lambda: uid("exam"))

@dataclass
class Assessment:
    student_id: str
    exam_id: str
    score: float
    max_score: float
    rubric: Dict[str, float] = field(default_factory=dict)
    teacher_reviewed: bool = False
    id: str = field(default_factory=lambda: uid("assessment"))

@dataclass
class LearningAnalytics:
    student_id: str
    strengths: List[str] = field(default_factory=list)
    weak_topics: List[str] = field(default_factory=list)
    progress: Dict[str, float] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uid("analytics"))
