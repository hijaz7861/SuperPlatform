from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DepartmentTask:
    task_id: str
    department: str
    action: str
    payload: Dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"
    requires_approval: bool = False
    approved: bool = False


@dataclass
class DepartmentDecision:
    action: str
    status: str
    reason: str
    requires_approval: bool = False


@dataclass
class DepartmentSnapshot:
    department: str
    students: int
    teachers: int
    pending_tasks: int
    alerts: List[str] = field(default_factory=list)
