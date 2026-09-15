# SUPERPLATFORM_TEST_ROOT
import sys
from pathlib import Path
_TEST_ROOT = Path(__file__).resolve().parents[4]
if str(_TEST_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEST_ROOT))


from core.autonomous.software_engineering.engine.software_engine_engine import (
    AutonomousSoftwareEngine,
)


def test_software_lifecycle():
    e = AutonomousSoftwareEngine()
    t = e.plan("s1", "build module")
    e.start(t)
    e.complete(t)
    assert t.status == "COMPLETED"
