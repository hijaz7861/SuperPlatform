# SUPERPLATFORM_TEST_ROOT
import sys
from pathlib import Path
_TEST_ROOT = Path(__file__).resolve().parents[4]
if str(_TEST_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEST_ROOT))


from core.autonomous.self_healing.engine.self_healing_engine import SelfHealingEngine


def test_self_healing():
    e = SelfHealingEngine()
    t = e.detect("r1", "component")
    e.repair(t)
    e.verify(t, True)
    assert t.status == "VERIFIED"
