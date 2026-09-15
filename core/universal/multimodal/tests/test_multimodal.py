import pytest

from core.universal.multimodal.engine.multimodal_engine import (
    MultimodalEngine,
)


def test_text():
    e = MultimodalEngine()
    x = e.create("1", "text", "hello")
    r = e.process(x)

    assert r.status == "PROCESSED"
    assert r.detected_type == "text"


def test_image():
    e = MultimodalEngine()
    x = e.create("2", "image", "image-data")
    r = e.process(x)

    assert r.detected_type == "image"


def test_document():
    e = MultimodalEngine()
    x = e.create("3", "document", "document-data")
    r = e.process(x)

    assert r.detected_type == "document"


def test_invalid():
    e = MultimodalEngine()
    x = e.create("4", "unknown", "x")

    with pytest.raises(ValueError):
        e.process(x)
