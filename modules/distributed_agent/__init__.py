"""Distributed Agent - swarm of workers for massive parallel search."""
from .coordinator import Coordinator
from .worker import Worker
from .task_queue import TaskQueue
from .aggregator import Aggregator

__all__ = ["Coordinator", "Worker", "TaskQueue", "Aggregator"]
