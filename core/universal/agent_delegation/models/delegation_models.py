
from dataclasses import dataclass


@dataclass
class DelegationTask:
    task_id: str
    source_agent: str
    target_agent: str
    status: str = "PENDING"
