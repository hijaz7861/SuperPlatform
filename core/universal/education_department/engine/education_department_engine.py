from ..models.department_models import (
    DepartmentDecision,
    DepartmentSnapshot,
    DepartmentTask,
)
from ..policies.department_policy import EducationDepartmentPolicy


class EducationDepartmentEngine:

    def create_task(
        self,
        task_id,
        action,
        payload=None,
        department="education",
    ):
        if not EducationDepartmentPolicy.allowed_department(
            department
        ):
            raise ValueError("INVALID_EDUCATION_DEPARTMENT")

        return DepartmentTask(
            task_id=task_id,
            department=department,
            action=action,
            payload=payload or {},
            requires_approval=(
                EducationDepartmentPolicy
                .requires_approval(action)
            ),
        )

    def execute_task(self, task):
        if (
            task.requires_approval
            and not task.approved
        ):
            raise PermissionError(
                "APPROVAL_REQUIRED_BEFORE_EXECUTION"
            )

        task.status = "COMPLETED"

        return task

    def approve_task(self, task):
        task.approved = True
        return task

    def analyze_department(
        self,
        students,
        teachers,
        pending_tasks=0,
        alerts=None,
    ):
        alerts = list(alerts or [])

        if students < 0 or teachers < 0:
            raise ValueError(
                "COUNTS_MUST_BE_NON_NEGATIVE"
            )

        if pending_tasks < 0:
            raise ValueError(
                "PENDING_TASKS_MUST_BE_NON_NEGATIVE"
            )

        return DepartmentSnapshot(
            department="education",
            students=students,
            teachers=teachers,
            pending_tasks=pending_tasks,
            alerts=alerts,
        )

    def recommend_actions(
        self,
        snapshot,
    ):
        recommendations = []

        if snapshot.pending_tasks > 0:
            recommendations.append(
                "Review pending academic tasks."
            )

        if snapshot.alerts:
            recommendations.append(
                "Review active education alerts."
            )

        if not recommendations:
            recommendations.append(
                "No immediate departmental action required."
            )

        return recommendations

    def decide(
        self,
        action,
        reason="",
    ):
        required = (
            EducationDepartmentPolicy
            .requires_approval(action)
        )

        return DepartmentDecision(
            action=action,
            status=(
                "AWAITING_APPROVAL"
                if required
                else "READY"
            ),
            reason=reason,
            requires_approval=required,
        )
