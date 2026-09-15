from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DynamicOption:
    option_id: str
    name: str
    value_type: str = "string"
    default: Any = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1


@dataclass
class OptionVersion:
    option_id: str
    version: int
    snapshot: Dict[str, Any]


@dataclass
class OptionAudit:
    action: str
    option_id: str
    version: int
    details: Dict[str, Any] = field(default_factory=dict)
