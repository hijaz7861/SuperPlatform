
"""
SuperPlatform Universal Policy Engine
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class PolicyResult:
    allowed: bool
    reason: str
    approval_required: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class UniversalPolicyEngine:

    def __init__(self):
        self.policies: Dict[str, Callable[..., PolicyResult]] = {}

    def register(self, name: str, policy: Callable[..., PolicyResult]):
        if not name:
            raise ValueError("Policy name required")
        if not callable(policy):
            raise TypeError("Policy must be callable")
        self.policies[name] = policy

    def evaluate(self, name: str, **context) -> PolicyResult:
        if name not in self.policies:
            return PolicyResult(
                allowed=False,
                reason=f"Policy not registered: {name}",
            )

        result = self.policies[name](**context)

        if not isinstance(result, PolicyResult):
            raise TypeError(
                "Policy must return PolicyResult"
            )

        return result

    def evaluate_all(self, **context) -> List[PolicyResult]:
        return [
            policy(**context)
            for policy in self.policies.values()
        ]
