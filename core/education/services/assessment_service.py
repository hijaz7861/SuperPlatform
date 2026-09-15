from core.education.models.education_models import Assessment

class AssessmentService:
    def __init__(self):
        self.assessments = {}

    def create(
        self,
        student_id,
        exam_id,
        score,
        max_score,
        rubric=None,
    ):
        if max_score <= 0:
            raise ValueError("INVALID_MAX_SCORE")

        if score < 0 or score > max_score:
            raise ValueError("INVALID_SCORE")

        item = Assessment(
            student_id=student_id,
            exam_id=exam_id,
            score=score,
            max_score=max_score,
            rubric=rubric or {},
        )

        self.assessments[item.id] = item
        return item

    def teacher_review(self, assessment_id):
        item = self.assessments[assessment_id]
        item.teacher_reviewed = True
        return item
