
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Agent:
    agent_id: str
    name: str
    department: str
    capabilities: List[str] = field(default_factory=list)
    enabled: bool = True
    status: str = "idle"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentTask:
    task_id: str
    title: str
    department: str
    requested_by: str = "system"
    priority: int = 50
    status: str = "queued"
    assigned_agent: str | None = None
    result: Any = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    approval_required: bool = False
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class KnowledgeItem:
    knowledge_id: str
    topic: str
    content: Any
    source: str
    verified: bool = False
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
