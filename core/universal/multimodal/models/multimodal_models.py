from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MultimodalInput:
    input_id: str
    input_type: str
    payload: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MultimodalResult:
    input_id: str
    detected_type: str
    status: str
    data: Dict[str, Any]
