
from core.universal.content_intelligence.engines.content_intelligence_engine import (
    UniversalContentIntelligence,
)
from core.universal.content_intelligence.policies.content_policy import (
    ContentIntelligencePolicy,
)


class ContentIntelligenceService:

    def __init__(self):
        self.engine = UniversalContentIntelligence()

    def analyze(self, content):
        return self.engine.analyze(content)

    def execute(
        self,
        action,
        approved=False,
    ):
        if not ContentIntelligencePolicy.can_execute(
            action,
            approved,
        ):
            raise PermissionError(
                "CONTENT_REVIEW_REQUIRED"
            )

        return {
            "action": action,
            "executed": True,
            "approved": approved,
        }
