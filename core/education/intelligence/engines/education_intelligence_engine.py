from core.education.intelligence.models.education_intelligence_models import (
    TopicPerformance,
    LearningPlan,
    RemediationTask,
    IntelligenceResult,
)


class EducationIntelligenceEngine:

    WEAK_THRESHOLD = 0.60

    def detect_weak_topics(self, performances):
        weak = []

        for item in performances:
            if item.score < self.WEAK_THRESHOLD:
                weak.append(item.topic)

        return list(dict.fromkeys(weak))

    def build_learning_plan(
        self,
        student_id,
        performances,
        goals=None,
    ):
        weak_topics = self.detect_weak_topics(performances)

        actions = []

        for topic in weak_topics:
            actions.append(
                f"remediate:{topic}"
            )

        return LearningPlan(
            student_id=student_id,
            goals=list(goals or []),
            weak_topics=weak_topics,
            recommended_actions=actions,
            status="draft",
        )

    def create_remediation_tasks(
        self,
        student_id,
        weak_topics,
    ):
        tasks = []

        for topic in weak_topics:
            tasks.append(
                RemediationTask(
                    student_id=student_id,
                    topic=topic,
                    action="review_and_practice",
                    priority="high",
                )
            )

        return tasks

    def analyze_student(
        self,
        student_id,
        performances,
        goals=None,
    ):
        plan = self.build_learning_plan(
            student_id,
            performances,
            goals,
        )

        tasks = self.create_remediation_tasks(
            student_id,
            plan.weak_topics,
        )

        confidence = 1.0 if performances else 0.0

        return IntelligenceResult(
            action="analyze_student",
            student_id=student_id,
            data={
                "learning_plan": plan,
                "remediation_tasks": tasks,
            },
            confidence=confidence,
            requires_review=bool(plan.weak_topics),
        )
