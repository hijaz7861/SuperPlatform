# SUPERPLATFORM_TEST_ROOT
import sys
from pathlib import Path
_TEST_ROOT = Path(__file__).resolve().parents[4]
if str(_TEST_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEST_ROOT))


from core.autonomous.continuous_improvement.engine.continuous_improvement_engine import (
    ContinuousImprovementEngine,
)


def test_improvement():
    e = ContinuousImprovementEngine()
    i = e.propose("i1", "improve component")
    e.evaluate(i, True)
    e.verify(i, True)
    assert i.status == "VERIFIED"


def test_rejected_improvement():
    e = ContinuousImprovementEngine()
    i = e.propose("i2", "unsafe change")
    e.evaluate(i, False)
    e.verify(i, True)
    assert i.status == "REJECTED"
