class AcademicAgentPolicy:

    # High-impact actions require explicit approval.
    # Generating an exam creates a DRAFT only.
    # Publishing the exam requires approval.
    APPROVAL_REQUIRED = {
        "publish_exam",
        "publish_assessment",
        "send_bulk_communication",
        "change_student_record",
        "delete_academic_data",
    }

    @classmethod
    def requires_approval(cls, action):
        return action in cls.APPROVAL_REQUIRED

    @classmethod
    def can_execute(cls, action, approved=False):
        if cls.requires_approval(action):
            return bool(approved)
        return True
