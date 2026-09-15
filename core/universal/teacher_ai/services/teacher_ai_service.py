
from core.universal.teacher_ai.engine.teacher_ai_engine import (
    TeacherAIEngine,
)
from core.universal.teacher_ai.policies.teacher_ai_policy import (
    TeacherAIPolicy,
)


class TeacherAIService:

    def __init__(
        self,
        content_intelligence=None,
        academic_intelligence=None,
    ):
        self.engine = TeacherAIEngine()
        self.content_intelligence = content_intelligence
        self.academic_intelligence = academic_intelligence

    def request(
        self,
        teacher_id,
        intent,
        params,
    ):
        return self.engine.handle_request(
            teacher_id,
            intent,
            params,
        )

    def execute_action(
        self,
        action,
        approved=False,
    ):
        if not TeacherAIPolicy.can_execute(
            action,
            approved,
        ):
            raise PermissionError(
                "TEACHER_ACTION_APPROVAL_REQUIRED"
            )

        return {
            "action": action,
            "executed": True,
            "approved": approved,
        }

    def integration_status(self):
        return {
            "content_intelligence_connected":
                self.content_intelligence is not None,
            "academic_intelligence_connected":
                self.academic_intelligence is not None,
            "provider_independent": True,
        }
