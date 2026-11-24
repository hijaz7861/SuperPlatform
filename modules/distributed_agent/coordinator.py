"""Coordinator that manages N workers and distributes tasks."""
import threading
from .task_queue import TaskQueue
from .worker import Worker
from .aggregator import Aggregator


class Coordinator:
    def __init__(self, num_workers=100, handler=None):
        self.num_workers = num_workers
        self.queue = TaskQueue()
        self.aggregator = Aggregator()
        self.workers = [Worker(i, handler) for i in range(num_workers)]
        self._threads = []

    def submit_tasks(self, tasks):
        self.queue.push_many(tasks)

    def run(self, timeout=30):
        def worker_loop(w):
            while True:
                task = self.queue.pop(timeout=0.5)
                if task is None:
                    break
                res = w.process(task)
                self.aggregator.add(res)

        for w in self.workers:
            t = threading.Thread(target=worker_loop, args=(w,), daemon=True)
            t.start()
            self._threads.append(t)
        for t in self._threads:
            t.join(timeout=timeout)
        return self.aggregator.summary()

    def get_results(self):
        return self.aggregator.all_results()
