
import re

from core.universal.content_intelligence.models.content_models import (
    ContentAnalysis,
    ContentUnit,
    Topic,
    LearningObjective,
    GeneratedQuestion,
)


class UniversalContentIntelligence:

    DIFFICULTIES = {
        "easy",
        "medium",
        "hard",
    }

    LEVELS = {
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create",
    }

    def extract_topics(self, content: ContentUnit):
        text = content.text

        headings = re.findall(
            r"(?im)^(?:chapter|unit|lesson|topic)"
            r"\s+\d*\s*[:.-]?\s*(.+)$",
            text,
        )

        if headings:
            names = [
                h.strip()
                for h in headings
                if h.strip()
            ]
        else:
            sentences = [
                s.strip()
                for s in re.split(r"[.!?]", text)
                if s.strip()
            ]
            names = sentences[:5]

        unique = list(dict.fromkeys(names))

        return [
            Topic(
                name=name,
                evidence=[name],
            )
            for name in unique
        ]

    def generate_objectives(self, topics):
        objectives = []

        for topic in topics:
            objectives.append(
                LearningObjective(
                    objective=(
                        f"Explain the key concepts of "
                        f"{topic.name}"
                    ),
                    topic=topic.name,
                    cognitive_level="understand",
                )
            )

        return objectives

    def generate_questions(
        self,
        topics,
        difficulty="medium",
        cognitive_level="understand",
    ):
        if difficulty not in self.DIFFICULTIES:
            raise ValueError(
                f"INVALID_DIFFICULTY:{difficulty}"
            )

        if cognitive_level not in self.LEVELS:
            raise ValueError(
                f"INVALID_COGNITIVE_LEVEL:{cognitive_level}"
            )

        questions = []

        for topic in topics:
            questions.append(
                GeneratedQuestion(
                    question=(
                        f"What are the key concepts "
                        f"of {topic.name}?"
                    ),
                    topic=topic.name,
                    difficulty=difficulty,
                    cognitive_level=cognitive_level,
                    answer=(
                        f"Key concepts related to "
                        f"{topic.name}."
                    ),
                    source_evidence=topic.evidence,
                    verified=False,
                )
            )

        return questions

    def detect_duplicates(self, questions):
        seen = set()
        duplicates = []

        for q in questions:
            key = re.sub(
                r"\W+",
                " ",
                q.question.lower(),
            ).strip()

            if key in seen:
                duplicates.append(q)
            else:
                seen.add(key)

        return duplicates

    def verify_questions(self, questions):
        verified = []

        for q in questions:
            valid = bool(
                q.question.strip()
                and q.answer.strip()
                and q.topic.strip()
                and q.source_evidence
            )

            q.verified = valid
            verified.append(q)

        return verified

    def analyze(
        self,
        content: ContentUnit,
    ):
        topics = self.extract_topics(content)
        objectives = self.generate_objectives(topics)
        questions = self.generate_questions(topics)

        self.verify_questions(questions)

        confidence = (
            1.0
            if topics
            else 0.0
        )

        return ContentAnalysis(
            content_id=content.id,
            topics=topics,
            objectives=objectives,
            questions=questions,
            confidence=confidence,
            requires_review=True,
        )
