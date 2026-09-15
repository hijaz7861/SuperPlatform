import re

from ..models.document_models import (
    Document,
    DocumentSection,
    DocumentAnalysis,
)


class DocumentIntelligenceEngine:

    def ingest(self, document_id, title, content, metadata=None):
        return Document(
            document_id=document_id,
            title=title,
            content=content,
            metadata=metadata or {},
        )

    def analyze(self, document):
        lines = [
            x.strip()
            for x in document.content.splitlines()
            if x.strip()
        ]

        sections = []

        for line in lines:
            if line.lower().startswith(
                ("chapter ", "section ", "unit ", "lesson ")
            ):
                sections.append(
                    DocumentSection(
                        title=line,
                        content="",
                    )
                )

        words = document.content.split()

        topics = []

        for word in words:
            clean = re.sub(r"[^A-Za-z0-9_-]", "", word)
            if len(clean) >= 6 and clean.lower() not in topics:
                topics.append(clean.lower())

        return DocumentAnalysis(
            document_id=document.document_id,
            sections=sections,
            topics=topics[:20],
            word_count=len(words),
        )
