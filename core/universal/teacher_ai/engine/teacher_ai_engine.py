
from core.universal.teacher_ai.models.teacher_ai_models import (
    LessonPlan,
    TeacherRecommendation,
    TeacherAssistantResult,
)


class TeacherAIEngine:

    def create_lesson_plan(
        self,
        teacher_id,
        subject,
        class_name,
        topic,
    ):
        return LessonPlan(
            title=f"Lesson: {topic}",
            subject=subject,
            class_name=class_name,
            objectives=[
                f"Understand {topic}",
                f"Explain key concepts of {topic}",
                f"Apply {topic} in practice",
            ],
            activities=[
                "Introduction",
                "Guided explanation",
                "Student practice",
                "Discussion",
            ],
            assessment_ideas=[
                "Short formative assessment",
                "Practice questions",
            ],
            status="draft",
        )

    def create_recommendations(
        self,
        weak_topics,
    ):
        results = []

        for topic in weak_topics:
            results.append(
                TeacherRecommendation(
                    category="remediation",
                    recommendation=(
                        f"Provide additional practice "
                        f"for {topic}"
                    ),
                    priority="high",
                    evidence=[topic],
                )
            )

        return results

    def summarize_student_performance(
        self,
        student_id,
        performance_data,
    ):
        if not performance_data:
            return {
                "student_id": student_id,
                "summary": "No performance data available",
                "weak_topics": [],
            }

        weak_topics = [
            item["topic"]
            for item in performance_data
            if item.get("score", 0) < 0.60
        ]

        average = round(
            sum(
                item.get("score", 0)
                for item in performance_data
            ) / len(performance_data),
            6,
        )

        return {
            "student_id": student_id,
            "average_score": average,
            "weak_topics": list(
                dict.fromkeys(weak_topics)
            ),
            "summary": (
                "Performance analyzed with "
                "available evidence"
            ),
        }

    def handle_request(
        self,
        teacher_id,
        intent,
        params,
    ):
        if intent == "lesson_plan":
            plan = self.create_lesson_plan(
                teacher_id=teacher_id,
                subject=params["subject"],
                class_name=params["class_name"],
                topic=params["topic"],
            )

            return TeacherAssistantResult(
                teacher_id=teacher_id,
                intent=intent,
                output={
                    "lesson_plan": plan,
                },
                confidence=1.0,
                requires_approval=False,
            )

        if intent == "student_analysis":
            result = self.summarize_student_performance(
                params["student_id"],
                params.get("performance_data", []),
            )

            return TeacherAssistantResult(
                teacher_id=teacher_id,
                intent=intent,
                output=result,
                confidence=1.0,
                requires_approval=False,
            )

        if intent == "remediation":
            recommendations = self.create_recommendations(
                params.get("weak_topics", [])
            )

            return TeacherAssistantResult(
                teacher_id=teacher_id,
                intent=intent,
                output={
                    "recommendations": recommendations,
                },
                confidence=1.0,
                requires_approval=True,
            )

        raise ValueError(
            f"UNKNOWN_TEACHER_INTENT:{intent}"
        )
