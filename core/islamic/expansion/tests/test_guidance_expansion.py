# SUPERPLATFORM_TEST_ROOT
import sys
from pathlib import Path
_TEST_ROOT = Path(__file__).resolve().parents[4]
if str(_TEST_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEST_ROOT))


from core.islamic.expansion.engine.guidance_expansion_engine import (
    GuidanceExpansionEngine,
)


def test_review_gate():
    e = GuidanceExpansionEngine()
    c = e.create_case("c1", "topic")
    e.attach_evidence(c, "e1")
    e.finalize(c)
    assert c.status == "REVIEW_REQUIRED"


def test_human_approval():
    e = GuidanceExpansionEngine()
    c = e.create_case("c2", "topic")
    e.finalize(c, human_approved=True)
    assert c.status == "APPROVED_WITH_HUMAN_REVIEW"
