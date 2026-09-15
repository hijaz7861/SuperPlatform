class StudentAIPolicy:

    APPROVAL_REQUIRED = {
        "change_student_record",
        "submit_assessment",
        "send_external_message",
        "enroll_course",
        "delete_learning_data",
    }

    @classmethod
    def requires_approval(cls, action):
        return action in cls.APPROVAL_REQUIRED

    @classmethod
    def can_execute(cls, action, approved=False):
        if cls.requires_approval(action):
            return bool(approved)
        return True

    @classmethod
    def confidence_allowed(cls, confidence):
        return 0.0 <= float(confidence) <= 1.0
