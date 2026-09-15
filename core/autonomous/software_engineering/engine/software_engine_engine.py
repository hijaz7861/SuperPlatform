
from ..models.software_models import BuildTask


class AutonomousSoftwareEngine:

    def __init__(self):
        self.tasks = {}

    def plan(self, task_id, requirement):
        task = BuildTask(task_id, requirement)
        self.tasks[task_id] = task
        return task

    def start(self, task):
        task.status = "RUNNING"
        return task

    def complete(self, task):
        task.status = "COMPLETED"
        return task
