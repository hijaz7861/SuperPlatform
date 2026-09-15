
from ..models.delegation_models import DelegationTask


class DelegationEngine:

    def __init__(self):
        self.tasks = {}

    def delegate(self, task_id, source_agent, target_agent):
        task = DelegationTask(
            task_id=task_id,
            source_agent=source_agent,
            target_agent=target_agent,
        )
        self.tasks[task_id] = task
        return task

    def accept(self, task):
        task.status = "ACCEPTED"
        return task

    def complete(self, task):
        task.status = "COMPLETED"
        return task
