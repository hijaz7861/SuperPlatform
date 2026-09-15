
class TeacherAIPolicy:

    APPROVAL_REQUIRED = {
        "assign_remediation",
        "publish_lesson",
        "publish_questions",
        "modify_student_record",
        "send_bulk_message",
    }

    @classmethod
    def requires_approval(cls, action):
        return action in cls.APPROVAL_REQUIRED

    @classmethod
    def can_execute(
        cls,
        action,
        approved=False,
    ):
        if cls.requires_approval(action):
            return bool(approved)

        return True
