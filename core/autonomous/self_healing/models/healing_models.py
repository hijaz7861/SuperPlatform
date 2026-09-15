
from dataclasses import dataclass


@dataclass
class RepairTask:
    task_id: str
    target: str
    status: str = "DETECTED"
