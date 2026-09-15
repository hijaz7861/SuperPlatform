
from typing import Dict, List
from core.agents.models.agent_models import KnowledgeItem


class SharedKnowledgeBus:

    def __init__(self):
        self.items: Dict[str, KnowledgeItem] = {}

    def publish(self, item: KnowledgeItem):
        if not item.topic:
            raise ValueError("Knowledge topic required")

        if not item.source:
            raise ValueError("Knowledge source required")

        if not 0.0 <= item.confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")

        self.items[item.knowledge_id] = item

    def get(self, knowledge_id: str):
        return self.items.get(knowledge_id)

    def search(
        self,
        topic: str,
        verified_only: bool = False,
    ) -> List[KnowledgeItem]:

        results = []

        for item in self.items.values():

            if topic.lower() not in item.topic.lower():
                continue

            if verified_only and not item.verified:
                continue

            results.append(item)

        return results

    def verified(self) -> List[KnowledgeItem]:
        return [
            item
            for item in self.items.values()
            if item.verified
        ]

    def count(self) -> int:
        return len(self.items)
