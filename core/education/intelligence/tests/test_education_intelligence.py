from core.education.intelligence.models.education_intelligence_models import (
    TopicPerformance,
)
from core.education.intelligence.engines.education_intelligence_engine import (
    EducationIntelligenceEngine,
)
from core.education.intelligence.engines.autonomous_academic_workflow import (
    AutonomousAcademicWorkflow,
)
from core.education.intelligence.services.academic_intelligence_service import (
    AcademicIntelligenceService,
)


def test_weak_topic_detection():
    engine = EducationIntelligenceEngine()

    performances = [
        TopicPerformance(
            "student_1",
            "Algebra",
            0.40,
            2,
        ),
        TopicPerformance(
            "student_1",
            "Geometry",
            0.85,
            2,
        ),
    ]

    weak = engine.detect_weak_topics(performances)

    assert weak == ["Algebra"]


def test_learning_plan_generation():
    engine = EducationIntelligenceEngine()

    performances = [
        TopicPerformance(
            "student_1",
            "Algebra",
            0.35,
        ),
    ]

    plan = engine.build_learning_plan(
        "student_1",
        performances,
        ["Improve Mathematics"],
    )

    assert plan.student_id == "student_1"
    assert "Algebra" in plan.weak_topics
    assert "remediate:Algebra" in plan.recommended_actions
    assert plan.status == "draft"


def test_remediation_generation():
    engine = EducationIntelligenceEngine()

    tasks = engine.create_remediation_tasks(
        "student_1",
        ["Algebra", "Fractions"],
    )

    assert len(tasks) == 2
    assert tasks[0].priority == "high"
    assert tasks[1].topic == "Fractions"


def test_student_intelligence_analysis():
    service = AcademicIntelligenceService()

    result = service.analyze_student(
        "student_1",
        [
            TopicPerformance(
                "student_1",
                "Algebra",
                0.30,
            )
        ],
        ["Improve Mathematics"],
    )

    assert result.action == "analyze_student"
    assert result.student_id == "student_1"
    assert result.confidence == 1.0
    assert result.requires_review is True
    assert len(result.data["remediation_tasks"]) == 1


def test_workflow_progression():
    workflow = AutonomousAcademicWorkflow()

    state = workflow.start(
        "workflow_1",
        "student_1",
    )

    assert state.current_stage == "analysis"
    assert state.status == "active"

    state = workflow.advance(
        "workflow_1",
        "learning_plan",
    )

    assert state.current_stage == "learning_plan"

    state = workflow.advance(
        "workflow_1",
        "completed",
    )

    assert state.current_stage == "completed"
    assert state.status == "completed"


def test_high_impact_action_requires_review():
    service = AcademicIntelligenceService()

    try:
        service.execute_action(
            "change_learning_plan",
            approved=False,
        )
        assert False
    except PermissionError as exc:
        assert str(exc) == "ACADEMIC_REVIEW_REQUIRED"

    result = service.execute_action(
        "change_learning_plan",
        approved=True,
    )

    assert result["executed"] is True
    assert result["approved"] is True


def test_low_impact_analysis_does_not_require_review():
    service = AcademicIntelligenceService()

    result = service.execute_action(
        "analyze_student",
        approved=False,
    )

    assert result["executed"] is True
