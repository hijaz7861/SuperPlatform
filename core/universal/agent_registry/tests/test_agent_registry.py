# SUPERPLATFORM_TEST_ROOT
import sys
from pathlib import Path
_TEST_ROOT = Path(__file__).resolve().parents[4]
if str(_TEST_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEST_ROOT))


from core.universal.agent_registry.engine.agent_registry_engine import AgentRegistry


def test_register_and_find():
    r = AgentRegistry()
    r.register("a1", "education", "analysis")
    assert len(r.find("analysis")) == 1


def test_disable():
    r = AgentRegistry()
    r.register("a1", "education", "analysis")
    r.disable("a1")
    assert r.find("analysis") == []
