class EducationDepartmentPolicy:

    APPROVAL_REQUIRED = {
        "publish_exam",
        "change_student_record",
        "send_bulk_communication",
        "remove_student",
        "remove_teacher",
        "modify_grading_policy",
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

    @classmethod
    def allowed_department(cls, department):
        return department in {
            "education",
            "academic",
            "school",
            "college",
            "university",
        }
