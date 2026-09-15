
from ..models.improvement_models import Improvement


class ContinuousImprovementEngine:

    def __init__(self):
        self.items = {}

    def propose(self, improvement_id, description):
        item = Improvement(improvement_id, description)
        self.items[improvement_id] = item
        return item

    def evaluate(self, item, accepted):
        item.status = "ACCEPTED" if accepted else "REJECTED"
        return item

    def verify(self, item, passed):
        if item.status != "ACCEPTED":
            return item

        item.status = "VERIFIED" if passed else "FAILED"
        return item
