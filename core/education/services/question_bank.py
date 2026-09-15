from core.education.models.education_models import Question

class QuestionBank:
    def __init__(self):
        self.questions = {}

    def add(self, question: Question):
        self.questions[question.id] = question
        return question

    def find(self, subject=None, topic=None,
             difficulty=None, question_type=None):

        result = list(self.questions.values())

        if subject:
            result = [q for q in result if q.subject == subject]

        if topic:
            result = [q for q in result if q.topic == topic]

        if difficulty:
            result = [q for q in result if q.difficulty == difficulty]

        if question_type:
            result = [
                q for q in result
                if q.question_type == question_type
            ]

        return result
