from core.education.agents.models.academic_agent_models import (
    AcademicTask,
    AcademicAgentResult,
    LearningPlan,
)
from core.education.agents.policies.academic_agent_policy import (
    AcademicAgentPolicy,
)


class AcademicAgentEngine:

    def __init__(self):
        self.agents = {}
        self.handlers = {}
        self.tasks = {}
        self.audit_log = []

    def register_agent(self, name, capabilities):
        self.agents[name] = {
            "name": name,
            "capabilities": list(capabilities),
            "enabled": True,
        }
        self.audit_log.append({
            "event": "agent_registered",
            "agent": name,
        })
        return self.agents[name]

    def register_handler(self, action, handler):
        self.handlers[action] = handler

    def create_task(
        self,
        task_type,
        requester_id,
        parameters=None,
    ):
        task = AcademicTask(
            task_type=task_type,
            requester_id=requester_id,
            parameters=parameters or {},
            requires_approval=
                AcademicAgentPolicy.requires_approval(task_type),
        )

        self.tasks[task.id] = task

        self.audit_log.append({
            "event": "task_created",
            "task_id": task.id,
            "task_type": task_type,
        })

        return task

    def approve(self, task_id, approver_id):
        task = self.tasks[task_id]

        if not approver_id:
            raise PermissionError("APPROVER_REQUIRED")

        task.approved_by = approver_id
        task.status = "approved"

        self.audit_log.append({
            "event": "task_approved",
            "task_id": task_id,
            "approver_id": approver_id,
        })

        return task

    def execute(self, task_id):
        task = self.tasks[task_id]

        if task.requires_approval and not task.approved_by:
            raise PermissionError(
                "APPROVAL_REQUIRED_BEFORE_EXECUTION"
            )

        handler = self.handlers.get(task.task_type)

        if handler is None:
            raise LookupError(
                f"NO_HANDLER_FOR:{task.task_type}"
            )

        task.status = "running"

        result = handler(task.parameters)

        task.result = result
        task.status = "completed"

        self.audit_log.append({
            "event": "task_completed",
            "task_id": task_id,
            "task_type": task.task_type,
        })

        return AcademicAgentResult(
            task_id=task.id,
            agent="academic_agent",
            action=task.task_type,
            status="completed",
            data=result,
        )

    def health(self):
        return {
            "agent_engine": "ok",
            "registered_agents": len(self.agents),
            "registered_handlers": len(self.handlers),
            "tasks": len(self.tasks),
            "audit_events": len(self.audit_log),
        }


class AcademicWorkflow:

    def __init__(
        self,
        agent_engine,
        book_analyzer=None,
        question_bank=None,
        exam_engine=None,
        assessment_service=None,
        analytics_service=None,
    ):
        self.engine = agent_engine
        self.book_analyzer = book_analyzer
        self.question_bank = question_bank
        self.exam_engine = exam_engine
        self.assessment_service = assessment_service
        self.analytics_service = analytics_service

    def register_default_agents(self):
        self.engine.register_agent(
            "book_analysis_agent",
            ["analyze_book", "extract_topics"],
        )

        self.engine.register_agent(
            "exam_agent",
            ["generate_exam", "prepare_exam", "publish_exam"],
        )

        self.engine.register_agent(
            "assessment_agent",
            ["assess", "review"],
        )

        self.engine.register_agent(
            "learning_analytics_agent",
            ["analyze_progress", "identify_weak_topics"],
        )

        self.engine.register_agent(
            "academic_coordinator_agent",
            ["coordinate_workflow"],
        )

    def connect_handlers(self):

        if self.book_analyzer:

            def analyze_book(params):
                return self.book_analyzer.analyze(
                    params["book"]
                )

            self.engine.register_handler(
                "analyze_book",
                analyze_book,
            )

        if self.exam_engine:

            def generate_exam(params):
                exam = self.exam_engine.generate(
                    title=params["title"],
                    subject=params["subject"],
                    class_name=params["class_name"],
                    duration_minutes=params["duration_minutes"],
                    question_ids=params.get(
                        "question_ids",
                        [],
                    ),
                    total_marks=params["total_marks"],
                )

                return {
                    "exam_id": exam.id,
                    "status": exam.status,
                    "approval_required_for_publish": True,
                }

            self.engine.register_handler(
                "generate_exam",
                generate_exam,
            )

            def publish_exam(params):
                exam = self.exam_engine.publish(
                    params["exam_id"]
                )

                return {
                    "exam_id": exam.id,
                    "status": exam.status,
                }

            self.engine.register_handler(
                "publish_exam",
                publish_exam,
            )

        if self.analytics_service:

            def analyze_progress(params):
                result = self.analytics_service.build(
                    params["student_id"],
                    params["assessments"],
                    params.get("topic_by_exam", {}),
                )

                return {
                    "student_id": result.student_id,
                    "strengths": result.strengths,
                    "weak_topics": result.weak_topics,
                    "progress": result.progress,
                }

            self.engine.register_handler(
                "analyze_progress",
                analyze_progress,
            )
