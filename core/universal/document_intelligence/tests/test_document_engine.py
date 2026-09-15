from core.universal.document_intelligence.engine.document_engine import (
    DocumentIntelligenceEngine,
)


def test_document_ingestion():
    e = DocumentIntelligenceEngine()

    d = e.ingest(
        "doc1",
        "Mathematics",
        "Chapter 1 Algebra\nVariables and equations.",
    )

    assert d.document_id == "doc1"
    assert d.title == "Mathematics"


def test_document_analysis():
    e = DocumentIntelligenceEngine()

    d = e.ingest(
        "doc1",
        "Book",
        "Chapter 1 Algebra\nVariables equations mathematics.",
    )

    a = e.analyze(d)

    assert a.document_id == "doc1"
    assert a.word_count > 0
    assert len(a.sections) == 1
    assert "mathematics" in a.topics


def test_empty_document():
    e = DocumentIntelligenceEngine()

    d = e.ingest("empty", "Empty", "")
    a = e.analyze(d)

    assert a.word_count == 0
    assert a.sections == []
