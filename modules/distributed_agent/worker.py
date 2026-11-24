"""Worker agent that processes a single search task."""
import time, random


class Worker:
    def __init__(self, worker_id, handler=None):
        self.worker_id = worker_id
        self.handler = handler or self._default_handler
        self.processed = 0

    def _default_handler(self, task):
        # Simulate search work
        time.sleep(0.01)
        return {"worker": self.worker_id, "task": task, "result": f"found_{random.randint(1,100)}", "ok": True}

    def process(self, task):
        self.processed += 1
        try:
            return self.handler(task)
        except Exception as e:
            return {"worker": self.worker_id, "task": task, "error": str(e), "ok": False}
