
from ..models.healing_models import RepairTask


class SelfHealingEngine:

    def __init__(self):
        self.repairs = {}

    def detect(self, task_id, target):
        task = RepairTask(task_id, target)
        self.repairs[task_id] = task
        return task

    def repair(self, task):
        task.status = "REPAIRED"
        return task

    def verify(self, task, passed):
        task.status = "VERIFIED" if passed else "FAILED"
        return task
