from core.universal.research.engine.research_engine import (
    ResearchEngine,
)


def test_question():
    e = ResearchEngine()

    q = e.create_question(
        "q1",
        "What is AI?",
    )

    assert q.status == "OPEN"


def test_finding():
    e = ResearchEngine()

    q = e.create_question("q1", "Question")
    r = e.create_result(q)

    e.add_finding(
        r,
        "source",
        "claim",
        0.8,
    )

    assert len(r.findings) == 1


def test_unverified_requires_review():
    e = ResearchEngine()

    q = e.create_question("q1", "Question")
    r = e.create_result(q)

    e.add_finding(
        r,
        "source",
        "claim",
        0.8,
    )

    e.finalize(r)

    assert r.status == "REVIEW_REQUIRED"


def test_verified_research():
    e = ResearchEngine()

    q = e.create_question("q1", "Question")
    r = e.create_result(q)

    f = e.add_finding(
        r,
        "source",
        "claim",
        0.9,
    )

    e.verify_finding(f)
    e.finalize(r)

    assert r.status == "VERIFIED"
