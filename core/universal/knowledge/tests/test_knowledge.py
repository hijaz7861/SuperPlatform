from core.universal.knowledge.engine.knowledge_engine import (
    KnowledgeEngine,
)


def test_add():
    e = KnowledgeEngine()

    x = e.add(
        "1",
        "Python",
        "Python programming",
        "source1",
        0.9,
    )

    assert x.topic == "Python"
    assert x.confidence == 0.9
    assert x.verified is False


def test_verify():
    e = KnowledgeEngine()

    x = e.add(
        "1",
        "AI",
        "Artificial intelligence",
        "source",
    )

    e.verify(x)

    assert x.verified is True


def test_search():
    e = KnowledgeEngine()

    items = [
        e.add("1", "Python", "Programming", "s1"),
        e.add("2", "Islamic Finance", "Ledger", "s2"),
    ]

    result = e.search(items, "python")

    assert len(result) == 1
    assert result[0].item_id == "1"


def test_confidence_bounds():
    e = KnowledgeEngine()

    x = e.add(
        "1",
        "X",
        "Y",
        "Z",
        5,
    )

    assert x.confidence == 1.0
