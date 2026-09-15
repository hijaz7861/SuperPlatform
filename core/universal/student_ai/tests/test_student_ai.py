import pytest

from core.universal.student_ai.engine.student_ai_engine import (
    StudentAIEngine,
)
from core.universal.student_ai.services.student_ai_service import (
    StudentAIService,
)


def test_student_performance_analysis():
    engine = StudentAIEngine()

    result = engine.analyze_performance(
        "student_1",
        [
            {"topic": "Algebra", "score": 0.40},
            {"topic": "Geometry", "score": 0.80},
        ],
    )

    assert result.student_id == "student_1"
    assert result.status == "ANALYZED"
    assert result.data["average_score"] == 0.60
    assert "Algebra" in result.data["weak_topics"]
    assert "Geometry" in result.data["strong_topics"]


def test_learning_plan_generation():
    engine = StudentAIEngine()

    plan = engine.generate_learning_plan(
        "student_1",
        ["Algebra", "Physics"],
        ["Improve mathematics"],
    )

    assert plan.student_id == "student_1"
    assert plan.status == "DRAFT"
    assert plan.topics == ["Algebra", "Physics"]


def test_recommendations_generation():
    engine = StudentAIEngine()

    recommendations = engine.generate_recommendations(
        "student_1",
        ["Algebra"],
    )

    assert len(recommendations) == 1
    assert recommendations[0].topic == "Algebra"
    assert recommendations[0].priority == "HIGH"
    assert recommendations[0].confidence == 0.90


def test_empty_performance():
    engine = StudentAIEngine()

    result = engine.analyze_performance(
        "student_1",
        [],
    )

    assert result.status == "NO_DATA"
    assert result.data["average_score"] == 0.0
    assert result.data["weak_topics"] == []


def test_scores_are_normalized():
    engine = StudentAIEngine()

    result = engine.analyze_performance(
        "student_1",
        [
            {"topic": "A", "score": 2.0},
            {"topic": "B", "score": -1.0},
        ],
    )

    assert result.data["topics"][0]["score"] == 1.0
    assert result.data["topics"][1]["score"] == 0.0


def test_approval_gate():
    service = StudentAIService()

    with pytest.raises(PermissionError):
        service.handle(
            "student_1",
            "submit_assessment",
            {},
            approved=False,
        )

    # The action passes the approval gate once explicitly approved.
    with pytest.raises(ValueError):
        service.handle(
            "student_1",
            "submit_assessment",
            {},
            approved=True,
        )


def test_provider_independence():
    service = StudentAIService()

    result = service.handle(
        "student_1",
        "analyze_progress",
        {
            "performance": [
                {"topic": "Science", "score": 0.50},
                {"topic": "Math", "score": 0.90},
            ]
        },
    )

    assert result.status == "ANALYZED"
    assert "Science" in result.data["weak_topics"]
