import pytest

from core.universal.education_department.engine.education_department_engine import (
    EducationDepartmentEngine,
)
from core.universal.education_department.services.education_department_service import (
    EducationDepartmentService,
)


def test_department_task_creation():
    engine = EducationDepartmentEngine()

    task = engine.create_task(
        "task_1",
        "analyze_progress",
    )

    assert task.task_id == "task_1"
    assert task.department == "education"
    assert task.status == "PENDING"
    assert task.requires_approval is False


def test_high_impact_task_requires_approval():
    engine = EducationDepartmentEngine()

    task = engine.create_task(
        "task_2",
        "publish_exam",
    )

    assert task.requires_approval is True

    with pytest.raises(PermissionError):
        engine.execute_task(task)


def test_approval_then_execution():
    engine = EducationDepartmentEngine()

    task = engine.create_task(
        "task_3",
        "publish_exam",
    )

    engine.approve_task(task)
    result = engine.execute_task(task)

    assert result.approved is True
    assert result.status == "COMPLETED"


def test_department_snapshot():
    engine = EducationDepartmentEngine()

    snapshot = engine.analyze_department(
        students=100,
        teachers=10,
        pending_tasks=4,
        alerts=["Low attendance"],
    )

    assert snapshot.department == "education"
    assert snapshot.students == 100
    assert snapshot.teachers == 10
    assert snapshot.pending_tasks == 4
    assert snapshot.alerts == ["Low attendance"]


def test_department_recommendations():
    engine = EducationDepartmentEngine()

    snapshot = engine.analyze_department(
        students=50,
        teachers=5,
        pending_tasks=2,
        alerts=["Performance alert"],
    )

    recommendations = engine.recommend_actions(
        snapshot
    )

    assert len(recommendations) == 2
    assert "pending academic tasks" in recommendations[0]
    assert "education alerts" in recommendations[1]


def test_safe_department_decision():
    engine = EducationDepartmentEngine()

    decision = engine.decide(
        "analyze_progress",
        "Routine student analysis",
    )

    assert decision.status == "READY"
    assert decision.requires_approval is False


def test_high_impact_department_decision():
    engine = EducationDepartmentEngine()

    decision = engine.decide(
        "send_bulk_communication",
        "Notify all students",
    )

    assert decision.status == "AWAITING_APPROVAL"
    assert decision.requires_approval is True


def test_service_coordinator():
    service = EducationDepartmentService()

    snapshot = service.snapshot(
        students=20,
        teachers=3,
        pending_tasks=0,
    )

    assert snapshot.students == 20
    assert snapshot.teachers == 3

    recommendations = service.recommendations(
        snapshot
    )

    assert len(recommendations) == 1
    assert "No immediate" in recommendations[0]
