from ..engine.student_ai_engine import StudentAIEngine
from ..policies.student_ai_policy import StudentAIPolicy


class StudentAIService:

    def __init__(self):
        self.engine = StudentAIEngine()

    def handle(self, student_id, action, payload=None, approved=False):
        payload = payload or {}

        if not StudentAIPolicy.can_execute(
            action,
            approved=approved,
        ):
            raise PermissionError(
                "APPROVAL_REQUIRED_BEFORE_EXECUTION"
            )

        if action == "analyze_progress":
            result = self.engine.analyze_performance(
                student_id,
                payload.get("performance", []),
            )
            return result

        if action == "generate_learning_plan":
            return self.engine.generate_learning_plan(
                student_id,
                payload.get("weak_topics", []),
                payload.get("goals", []),
            )

        if action == "generate_recommendations":
            return self.engine.generate_recommendations(
                student_id,
                payload.get("weak_topics", []),
            )

        raise ValueError(
            f"UNSUPPORTED_STUDENT_AI_ACTION: {action}"
        )
