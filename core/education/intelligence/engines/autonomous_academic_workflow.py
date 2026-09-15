from core.education.intelligence.models.education_intelligence_models import (
    AcademicWorkflowState,
)


class AutonomousAcademicWorkflow:

    STAGES = [
        "analysis",
        "learning_plan",
        "remediation",
        "teacher_review",
        "approved",
        "completed",
    ]

    def __init__(self):
        self.workflows = {}

    def start(self, workflow_id, student_id):
        state = AcademicWorkflowState(
            workflow_id=workflow_id,
            student_id=student_id,
            stages=list(self.STAGES),
            current_stage="analysis",
            status="active",
        )

        self.workflows[workflow_id] = state
        return state

    def advance(self, workflow_id, stage):
        state = self.workflows[workflow_id]

        if stage not in self.STAGES:
            raise ValueError(
                f"UNKNOWN_STAGE:{stage}"
            )

        state.current_stage = stage

        if stage == "completed":
            state.status = "completed"

        return state
