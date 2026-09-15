
from typing import Dict, List
from core.islamic.models.islamic_models import (
    SourceReference,
    EvidenceItem,
)


class IslamicKnowledgeRegistry:

    def __init__(self):
        self.sources: Dict[str, SourceReference] = {}
        self.evidence: Dict[str, EvidenceItem] = {}

    def register_source(self, source: SourceReference):
        if not source.source_id:
            raise ValueError("Source ID required")

        if not source.title:
            raise ValueError("Source title required")

        if not source.source_type:
            raise ValueError("Source type required")

        self.sources[source.source_id] = source

    def add_evidence(self, item: EvidenceItem):
        if item.source.source_id not in self.sources:
            raise ValueError(
                "Evidence source must be registered first"
            )

        self.evidence[item.evidence_id] = item

    def get_source(self, source_id: str):
        return self.sources.get(source_id)

    def get_evidence(self, evidence_id: str):
        return self.evidence.get(evidence_id)

    def search(self, text: str) -> List[EvidenceItem]:
        text = text.lower()

        return [
            item
            for item in self.evidence.values()
            if (
                text in item.excerpt.lower()
                or text in item.source.title.lower()
                or text in item.source.locator.lower()
            )
        ]

    def verified_evidence(self) -> List[EvidenceItem]:
        return [
            item
            for item in self.evidence.values()
            if item.verified
        ]

    def counts(self):
        return {
            "sources": len(self.sources),
            "evidence": len(self.evidence),
            "verified_evidence": len(self.verified_evidence()),
        }
