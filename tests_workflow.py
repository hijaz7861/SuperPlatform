import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from workflow_loop import WorkflowLoop


def test_workflow_cycle():
    loop = WorkflowLoop()
    report, drafts = loop.run_cycle("techsupport", 3)
    assert report["problems_found"] == 3
    assert report["solutions_drafted"] == 3
    assert report["quota_ok"] is True


if __name__ == "__main__":
    test_workflow_cycle()
    print("WORKFLOW LOOP TEST: PASS")
