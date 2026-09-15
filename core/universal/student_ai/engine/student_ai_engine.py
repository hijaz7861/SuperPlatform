from ..models.student_ai_models import (
    StudentLearningPlan,
    StudentRecommendation,
    StudentAssistantResult,
)


class StudentAIEngine:

    def analyze_performance(self, student_id, performance_data):
        if not performance_data:
            return StudentAssistantResult(
                student_id=student_id,
                action="analyze_progress",
                status="NO_DATA",
                data={
                    "average_score": 0.0,
                    "weak_topics": [],
                    "strong_topics": [],
                },
            )

        normalized = []

        for item in performance_data:
            topic = str(item.get("topic", "")).strip()
            score = float(item.get("score", 0.0))

            score = max(0.0, min(1.0, score))

            normalized.append({
                "topic": topic,
                "score": score,
            })

        average = round(
            sum(item["score"] for item in normalized)
            / len(normalized),
            6,
        )

        weak_topics = [
            item["topic"]
            for item in normalized
            if item["score"] < 0.60
        ]

        strong_topics = [
            item["topic"]
            for item in normalized
            if item["score"] >= 0.80
        ]

        return StudentAssistantResult(
            student_id=student_id,
            action="analyze_progress",
            status="ANALYZED",
            data={
                "average_score": average,
                "weak_topics": weak_topics,
                "strong_topics": strong_topics,
                "topics": normalized,
            },
        )

    def generate_learning_plan(
        self,
        student_id,
        weak_topics,
        goals=None,
    ):
        goals = goals or []

        priorities = list(weak_topics)

        return StudentLearningPlan(
            student_id=student_id,
            goals=goals,
            topics=list(weak_topics),
            priorities=priorities,
            status="DRAFT",
        )

    def generate_recommendations(
        self,
        student_id,
        weak_topics,
    ):
        recommendations = []

        for topic in weak_topics:
            recommendations.append(
                StudentRecommendation(
                    student_id=student_id,
                    topic=topic,
                    recommendation=(
                        f"Review {topic}, practice targeted "
                        "questions, and reassess progress."
                    ),
                    priority="HIGH",
                    confidence=0.90,
                )
            )

        return recommendations
