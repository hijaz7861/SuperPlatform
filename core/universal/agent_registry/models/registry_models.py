
from dataclasses import dataclass


@dataclass
class AgentRecord:
    agent_id: str
    department: str
    capability: str
    enabled: bool = True
