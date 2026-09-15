import re

from core.education.models.education_models import (
    BookDocument,
    Topic,
)


class BookAnalyzer:
    """
    Provider-independent deterministic book/document analyzer.

    This is a foundation component. It does not claim
    LLM/OCR-level intelligence.
    """

    def analyze(self, book: BookDocument):
        text = book.text.strip()

        words = re.findall(r"\b[\w'-]+\b", text)

        sentences = [
            x.strip()
            for x in re.split(r"[.!?]+", text)
            if x.strip()
        ]

        # Detect Chapter / Unit / Lesson headings both when
        # they occur on separate lines and when the entire
        # document is provided as one continuous line.
        heading_pattern = (
            r"(?i)(?:chapter|unit|lesson)"
            r"\s+\d+"
            r"(?:\s+[^.!?\n]*?)?"
            r"(?=\s*(?:\.|$))"
        )

        chapters = [
            match.group(0).strip()
            for match in re.finditer(
                heading_pattern,
                text,
            )
        ]

        # Deterministic keyword foundation.
        keywords = sorted(
            {
                word.lower()
                for word in words
                if len(word) >= 5
            }
        )[:30]

        # Simple deterministic summary foundation.
        summary = " ".join(sentences[:3])

        return {
            "book_id": book.id,
            "title": book.title,
            "word_count": len(words),
            "sentence_count": len(sentences),
            "chapters": chapters,
            "keywords": keywords,
            "summary": summary,
            "provider_independent": True,
        }

    def extract_topics(self, book: BookDocument):
        result = self.analyze(book)

        topics = []

        for chapter in result["chapters"]:
            topics.append(
                Topic(
                    book_id=book.id,
                    title=chapter,
                    chapter=chapter,
                    keywords=result["keywords"][:10],
                )
            )

        return topics
