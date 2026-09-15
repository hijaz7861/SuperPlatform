from ..models.knowledge_models import KnowledgeItem


class KnowledgeEngine:

    def add(
        self,
        item_id,
        topic,
        content,
        source,
        confidence=0.0,
        verified=False,
    ):
        confidence = round(
            max(0.0, min(1.0, float(confidence))),
            6,
        )

        return KnowledgeItem(
            item_id=item_id,
            topic=topic,
            content=content,
            source=source,
            confidence=confidence,
            verified=verified,
        )

    def verify(self, item):
        item.verified = True
        return item

    def search(self, items, topic):
        topic = topic.lower()

        return [
            x for x in items
            if topic in x.topic.lower()
            or topic in x.content.lower()
        ]
