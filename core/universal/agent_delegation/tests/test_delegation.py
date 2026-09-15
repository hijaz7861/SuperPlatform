# SUPERPLATFORM_TEST_ROOT
import sys
from pathlib import Path
_TEST_ROOT = Path(__file__).resolve().parents[4]
if str(_TEST_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEST_ROOT))


from core.universal.agent_delegation.engine.delegation_engine import DelegationEngine


def test_delegation_lifecycle():
    e = DelegationEngine()
    t = e.delegate("t1", "agent-a", "agent-b")
    e.accept(t)
    e.complete(t)
    assert t.status == "COMPLETED"
