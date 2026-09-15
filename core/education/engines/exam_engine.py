from core.education.models.education_models import Exam

class ExamEngine:
    def __init__(self, question_bank):
        self.question_bank = question_bank
        self.exams = {}

    def generate(
        self,
        title,
        subject,
        class_name,
        duration_minutes,
        question_ids,
        total_marks,
    ):
        exam = Exam(
            title=title,
            subject=subject,
            class_name=class_name,
            duration_minutes=duration_minutes,
            total_marks=total_marks,
            question_ids=list(question_ids),
            status="draft",
        )

        self.exams[exam.id] = exam
        return exam

    def approve(self, exam_id, approver_id):
        exam = self.exams[exam_id]

        if not approver_id:
            raise PermissionError("APPROVER_REQUIRED")

        exam.status = "approved"
        exam.approved_by = approver_id
        return exam

    def publish(self, exam_id):
        exam = self.exams[exam_id]

        if exam.status != "approved":
            raise PermissionError(
                "EXAM_APPROVAL_REQUIRED_BEFORE_PUBLISH"
            )

        exam.status = "published"
        return exam
