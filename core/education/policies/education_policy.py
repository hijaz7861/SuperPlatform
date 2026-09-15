class EducationPolicy:
    AI_GENERATED_EXAM_REQUIRES_APPROVAL = True
    PUBLISH_REQUIRES_APPROVAL = True
    TEACHER_REVIEW_SUPPORTED = True
    AUDIT_REQUIRED = True

    @classmethod
    def can_publish_exam(cls, exam):
        return (
            exam.status == "approved"
            and bool(exam.approved_by)
        )
