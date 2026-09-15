
from core.universal.teacher_ai.engine.teacher_ai_engine import (
    TeacherAIEngine,
)
from core.universal.teacher_ai.services.teacher_ai_service import (
    TeacherAIService,
)


def test_lesson_plan_generation():
    engine = TeacherAIEngine()

    plan = engine.create_lesson_plan(
        teacher_id="teacher_1",
        subject="Mathematics",
        class_name="Grade 8",
        topic="Algebra",
    )

    assert plan.title == "Lesson: Algebra"
    assert plan.subject == "Mathematics"
    assert plan.class_name == "Grade 8"
    assert len(plan.objectives) == 3
    assert len(plan.activities) >= 3
    assert plan.status == "draft"


def test_student_performance_analysis():
    engine = TeacherAIEngine()

    result = engine.summarize_student_performance(
        "student_1",
        [
            {"topic": "Algebra", "score": 0.40},
            {"topic": "Geometry", "score": 0.80},
        ],
    )

    assert result["student_id"] == "student_1"
    assert result["average_score"] == 0.60
    assert result["weak_topics"] == ["Algebra"]


def test_remediation_recommendation():
    engine = TeacherAIEngine()

    recommendations = engine.create_recommendations(
        ["Algebra", "Fractions"]
    )

    assert len(recommendations) == 2
    assert recommendations[0].priority == "high"
    assert recommendations[1].evidence == ["Fractions"]


def test_teacher_request_router():
    service = TeacherAIService()

    result = service.request(
        teacher_id="teacher_1",
        intent="lesson_plan",
        params={
            "subject": "Science",
            "class_name": "Grade 7",
            "topic": "Energy",
        },
    )

    assert result.teacher_id == "teacher_1"
    assert result.intent == "lesson_plan"
    assert result.confidence == 1.0
    assert result.requires_approval is False
    assert result.output["lesson_plan"].status == "draft"


def test_high_impact_teacher_action_requires_approval():
    service = TeacherAIService()

    try:
        service.execute_action(
            "assign_remediation",
            approved=False,
        )
        assert False
    except PermissionError as exc:
        assert str(exc) == (
            "TEACHER_ACTION_APPROVAL_REQUIRED"
        )

    result = service.execute_action(
        "assign_remediation",
        approved=True,
    )

    assert result["executed"] is True
    assert result["approved"] is True


def test_teacher_remediation_request_has_review_gate():
    service = TeacherAIService()

    result = service.request(
        teacher_id="teacher_1",
        intent="remediation",
        params={
            "weak_topics": ["Algebra"]
        },
    )

    assert result.requires_approval is True
    assert len(
        result.output["recommendations"]
    ) == 1


def test_teacher_integration_status():
    service = TeacherAIService(
        content_intelligence=object(),
        academic_intelligence=object(),
    )

    status = service.integration_status()

    assert status[
        "content_intelligence_connected"
    ] is True

    assert status[
        "academic_intelligence_connected"
    ] is True

    assert status[
        "provider_independent"
    ] is True
