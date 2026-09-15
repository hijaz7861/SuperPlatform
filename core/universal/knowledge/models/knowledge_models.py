from dataclasses import dataclass, field
from typing import Dict


@dataclass
class KnowledgeItem:
    item_id: str
    topic: str
    content: str
    source: str
    confidence: float = 0.0
    verified: bool = False
    metadata: Dict[str, str] = field(default_factory=dict)
