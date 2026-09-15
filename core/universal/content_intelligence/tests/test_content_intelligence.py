
from core.universal.content_intelligence.models.content_models import (
    ContentUnit,
)
from core.universal.content_intelligence.engines.content_intelligence_engine import (
    UniversalContentIntelligence,
)
from core.universal.content_intelligence.services.content_intelligence_service import (
    ContentIntelligenceService,
)


def test_topic_extraction():
    engine = UniversalContentIntelligence()

    content = ContentUnit(
        id="book1",
        title="Test Book",
        text=(
            "Chapter 1: Algebra\n"
            "Chapter 2: Geometry"
        ),
    )

    topics = engine.extract_topics(content)

    assert len(topics) == 2
    assert topics[0].name == "Algebra"
    assert topics[1].name == "Geometry"


def test_objective_generation():
    engine = UniversalContentIntelligence()

    content = ContentUnit(
        id="book1",
        title="Test",
        text="Chapter 1: Algebra",
    )

    topics = engine.extract_topics(content)
    objectives = engine.generate_objectives(topics)

    assert len(objectives) == 1
    assert objectives[0].topic == "Algebra"
    assert objectives[0].cognitive_level == "understand"


def test_question_generation():
    engine = UniversalContentIntelligence()

    content = ContentUnit(
        id="book1",
        title="Test",
        text="Chapter 1: Algebra",
    )

    topics = engine.extract_topics(content)

    questions = engine.generate_questions(
        topics,
        difficulty="hard",
        cognitive_level="analyze",
    )

    assert len(questions) == 1
    assert questions[0].difficulty == "hard"
    assert questions[0].cognitive_level == "analyze"
    assert questions[0].verified is False


def test_question_verification():
    engine = UniversalContentIntelligence()

    content = ContentUnit(
        id="book1",
        title="Test",
        text="Chapter 1: Algebra",
    )

    analysis = engine.analyze(content)

    assert len(analysis.questions) == 1
    assert analysis.questions[0].verified is True
    assert analysis.requires_review is True


def test_duplicate_detection():
    engine = UniversalContentIntelligence()

    content = ContentUnit(
        id="book1",
        title="Test",
        text="Chapter 1: Algebra",
    )

    topics = engine.extract_topics(content)

    questions = engine.generate_questions(topics)
    questions += engine.generate_questions(topics)

    duplicates = engine.detect_duplicates(questions)

    assert len(duplicates) == 1


def test_publish_requires_review():
    service = ContentIntelligenceService()

    try:
        service.execute(
            "publish_questions",
            approved=False,
        )
        assert False
    except PermissionError as exc:
        assert str(exc) == "CONTENT_REVIEW_REQUIRED"

    result = service.execute(
        "publish_questions",
        approved=True,
    )

    assert result["executed"] is True
    assert result["approved"] is True


def test_non_publish_analysis_does_not_require_approval():
    service = ContentIntelligenceService()

    result = service.execute(
        "analyze_content",
        approved=False,
    )

    assert result["executed"] is True
