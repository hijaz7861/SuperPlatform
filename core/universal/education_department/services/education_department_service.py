from ..engine.education_department_engine import (
    EducationDepartmentEngine,
)


class EducationDepartmentService:

    def __init__(self):
        self.engine = EducationDepartmentEngine()

    def create_task(
        self,
        task_id,
        action,
        payload=None,
    ):
        return self.engine.create_task(
            task_id=task_id,
            action=action,
            payload=payload,
        )

    def approve(self, task):
        return self.engine.approve_task(task)

    def execute(self, task):
        return self.engine.execute_task(task)

    def snapshot(
        self,
        students,
        teachers,
        pending_tasks=0,
        alerts=None,
    ):
        return self.engine.analyze_department(
            students=students,
            teachers=teachers,
            pending_tasks=pending_tasks,
            alerts=alerts,
        )

    def recommendations(self, snapshot):
        return self.engine.recommend_actions(snapshot)

    def decide(self, action, reason=""):
        return self.engine.decide(
            action=action,
            reason=reason,
        )
