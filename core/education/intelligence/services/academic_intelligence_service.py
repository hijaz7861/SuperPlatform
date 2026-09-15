from core.education.intelligence.engines.education_intelligence_engine import (
    EducationIntelligenceEngine,
)
from core.education.intelligence.engines.autonomous_academic_workflow import (
    AutonomousAcademicWorkflow,
)
from core.education.intelligence.policies.education_intelligence_policy import (
    EducationIntelligencePolicy,
)


class AcademicIntelligenceService:

    def __init__(self):
        self.engine = EducationIntelligenceEngine()
        self.workflow = AutonomousAcademicWorkflow()

    def analyze_student(
        self,
        student_id,
        performances,
        goals=None,
    ):
        return self.engine.analyze_student(
            student_id,
            performances,
            goals,
        )

    def start_workflow(
        self,
        workflow_id,
        student_id,
    ):
        return self.workflow.start(
            workflow_id,
            student_id,
        )

    def execute_action(
        self,
        action,
        approved=False,
    ):
        if not EducationIntelligencePolicy.can_execute(
            action,
            approved,
        ):
            raise PermissionError(
                "ACADEMIC_REVIEW_REQUIRED"
            )

        return {
            "action": action,
            "executed": True,
            "approved": approved,
        }
