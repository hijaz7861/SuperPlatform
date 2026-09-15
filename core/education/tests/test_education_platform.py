from core.education.models.education_models import (
    Teacher,
    Student,
    BookDocument,
    Question,
)
from core.education.services.teacher_service import TeacherService
from core.education.services.attendance_service import AttendanceService
from core.education.services.book_analyzer import BookAnalyzer
from core.education.services.question_bank import QuestionBank
from core.education.engines.exam_engine import ExamEngine
from core.education.services.assessment_service import AssessmentService
from core.education.services.analytics_service import AnalyticsService


def test_teacher_and_attendance():
    teachers = TeacherService()
    attendance = AttendanceService()

    teacher = teachers.register(
        Teacher(name="Teacher One")
    )

    teachers.assign_subject(teacher.id, "Mathematics")

    record = attendance.record(
        teacher.id,
        "2026-09-15",
        "present",
        "08:00",
        "14:00",
    )

    assert teacher.id == record.teacher_id
    assert teacher.subjects == ["Mathematics"]


def test_book_analysis():
    analyzer = BookAnalyzer()

    book = BookDocument(
        title="Sample Book",
        text=(
            "Chapter 1 Mathematics. "
            "Numbers and operations are important. "
            "Chapter 2 Algebra. "
            "Variables represent values."
        ),
    )

    result = analyzer.analyze(book)

    assert result["word_count"] > 0
    assert len(result["chapters"]) == 2
    assert result["provider_independent"] is True


def test_question_bank_and_exam_approval():
    bank = QuestionBank()

    q = bank.add(
        Question(
            text="What is 2 + 2?",
            question_type="mcq",
            difficulty="easy",
            subject="Mathematics",
            topic="Numbers",
            marks=1,
        )
    )

    assert len(bank.find(subject="Mathematics")) == 1

    exams = ExamEngine(bank)

    exam = exams.generate(
        "Math Test",
        "Mathematics",
        "Grade 5",
        60,
        [q.id],
        1,
    )

    try:
        exams.publish(exam.id)
        assert False
    except PermissionError:
        pass

    exams.approve(exam.id, "teacher_admin")
    exams.publish(exam.id)

    assert exam.status == "published"


def test_assessment_and_analytics():
    bank = QuestionBank()
    exams = ExamEngine(bank)

    exam = exams.generate(
        "Science Test",
        "Science",
        "Grade 5",
        45,
        [],
        100,
    )

    assessments = AssessmentService()

    a = assessments.create(
        "student_1",
        exam.id,
        85,
        100,
    )

    analytics = AnalyticsService()

    result = analytics.build(
        "student_1",
        [a],
        {exam.id: "Science"},
    )

    assert result.progress["Science"] == 85.0
    assert "Science" in result.strengths


def test_student_model():
    student = Student(
        name="Student One",
        class_name="Grade 5",
        subjects=["Science"],
    )

    assert student.class_name == "Grade 5"
    assert "Science" in student.subjects
