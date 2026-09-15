
from dataclasses import dataclass


@dataclass
class BuildTask:
    task_id: str
    requirement: str
    status: str = "PLANNED"
