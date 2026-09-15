
class ContentIntelligencePolicy:

    REVIEW_REQUIRED = {
        "publish_content",
        "publish_questions",
        "publish_exam",
        "send_academic_content",
    }

    @classmethod
    def requires_review(cls, action):
        return action in cls.REVIEW_REQUIRED

    @classmethod
    def can_execute(
        cls,
        action,
        approved=False,
    ):
        if cls.requires_review(action):
            return bool(approved)

        return True
