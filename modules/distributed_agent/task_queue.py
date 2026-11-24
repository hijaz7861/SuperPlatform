"""Thread-safe task queue for distributed workers."""
import queue, threading


class TaskQueue:
    def __init__(self):
        self._q = queue.Queue()
        self._lock = threading.Lock()

    def push(self, task):
        self._q.put(task)

    def pop(self, timeout=1):
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return None

    def size(self):
        return self._q.qsize()

    def push_many(self, tasks):
        for t in tasks:
            self.push(t)
