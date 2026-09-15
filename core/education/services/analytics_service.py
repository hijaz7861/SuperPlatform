from collections import defaultdict
from core.education.models.education_models import LearningAnalytics

class AnalyticsService:
    def build(self, student_id, assessments, topic_by_exam=None):
        topic_by_exam = topic_by_exam or {}

        scores = defaultdict(list)

        for item in assessments:
            percentage = (
                item.score / item.max_score * 100
                if item.max_score else 0
            )

            topic = topic_by_exam.get(
                item.exam_id,
                "general"
            )

            scores[topic].append(percentage)

        progress = {
            topic: round(sum(values) / len(values), 2)
            for topic, values in scores.items()
        }

        strengths = [
            topic for topic, value in progress.items()
            if value >= 80
        ]

        weak_topics = [
            topic for topic, value in progress.items()
            if value < 50
        ]

        return LearningAnalytics(
            student_id=student_id,
            strengths=strengths,
            weak_topics=weak_topics,
            progress=progress,
        )
