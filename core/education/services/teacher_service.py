from core.education.models.education_models import Teacher

class TeacherService:
    def __init__(self):
        self.teachers = {}

    def register(self, teacher: Teacher) -> Teacher:
        self.teachers[teacher.id] = teacher
        return teacher

    def get(self, teacher_id: str):
        return self.teachers.get(teacher_id)

    def assign_subject(self, teacher_id: str, subject: str):
        teacher = self.teachers[teacher_id]
        if subject not in teacher.subjects:
            teacher.subjects.append(subject)
        return teacher

    def assign_class(self, teacher_id: str, class_name: str):
        teacher = self.teachers[teacher_id]
        if class_name not in teacher.classes:
            teacher.classes.append(class_name)
        return teacher
