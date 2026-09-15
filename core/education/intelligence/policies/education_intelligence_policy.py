class EducationIntelligencePolicy:

    REVIEW_REQUIRED_ACTIONS = {
        "change_learning_plan",
        "assign_remediation",
        "publish_academic_content",
        "change_student_record",
    }

    @classmethod
    def requires_review(cls, action):
        return action in cls.REVIEW_REQUIRED_ACTIONS

    @classmethod
    def can_execute(cls, action, approved=False):
        if cls.requires_review(action):
            return bool(approved)

        return True
