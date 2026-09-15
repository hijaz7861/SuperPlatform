
from dataclasses import dataclass


@dataclass
class Improvement:
    improvement_id: str
    description: str
    status: str = "PROPOSED"
