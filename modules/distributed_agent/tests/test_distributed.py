import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.distributed_agent.coordinator import Coordinator
from modules.distributed_agent.aggregator import Aggregator


def test_coordinator_runs():
    c = Coordinator(num_workers=4)
    c.submit_tasks([{"id": i} for i in range(10)])
    s = c.run(timeout=10)
    assert s["total"] == 10
    assert s["success"] == 10
    assert s["workers_used"] <= 4


def test_aggregator():
    a = Aggregator()
    a.add({"worker": 1, "ok": True})
    a.add({"worker": 2, "ok": False})
    s = a.summary()
    assert s["total"] == 2
    assert s["success"] == 1
    assert s["failed"] == 1


if __name__ == "__main__":
    test_coordinator_runs()
    test_aggregator()
    print("DISTRIBUTED AGENT TESTS: PASS")
