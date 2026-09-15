from core.education.agents.engine.academic_agent_engine import (
    AcademicAgentEngine,
    AcademicWorkflow,
)
from core.education.agents.engine.academic_command_router import (
    AcademicCommandRouter,
)
from core.education.agents.models.academic_agent_models import (
    LearningPlan,
)
from core.education.models.education_models import (
    BookDocument,
)
from core.education.services.book_analyzer import BookAnalyzer
from core.education.services.analytics_service import AnalyticsService
from core.education.services.assessment_service import AssessmentService
from core.education.engines.exam_engine import ExamEngine
from core.education.services.question_bank import QuestionBank


def test_agent_registration_and_health():
    engine = AcademicAgentEngine()
    workflow = AcademicWorkflow(engine)

    workflow.register_default_agents()

    health = engine.health()

    assert health["registered_agents"] == 5
    assert health["agent_engine"] == "ok"


def test_book_agent_workflow():
    engine = AcademicAgentEngine()

    workflow = AcademicWorkflow(
        engine,
        book_analyzer=BookAnalyzer(),
    )

    workflow.register_default_agents()
    workflow.connect_handlers()

    book = BookDocument(
        title="AI Education",
        text=(
            "Chapter 1 Learning. "
            "Students learn concepts. "
            "Chapter 2 Assessment. "
            "Assessment measures progress."
        ),
    )

    task = engine.create_task(
        "analyze_book",
        "teacher_1",
        {"book": book},
    )

    result = engine.execute(task.id)

    assert result.status == "completed"
    assert result.data["word_count"] > 0
    assert len(result.data["chapters"]) == 2


def test_exam_agent_requires_approval():
    engine = AcademicAgentEngine()

    bank = QuestionBank()
    exams = ExamEngine(bank)

    workflow = AcademicWorkflow(
        engine,
        exam_engine=exams,
    )

    workflow.register_default_agents()
    workflow.connect_handlers()

    # --------------------------------------------------------
    # STEP 1: Generate exam as DRAFT.
    # Generation itself does not require approval.
    # --------------------------------------------------------

    task = engine.create_task(
        "generate_exam",
        "teacher_1",
        {
            "title": "Mathematics Test",
            "subject": "Mathematics",
            "class_name": "Grade 8",
            "duration_minutes": 60,
            "question_ids": [],
            "total_marks": 40,
        },
    )

    result = engine.execute(task.id)

    assert result.status == "completed"
    assert result.data["status"] == "draft"
    assert result.data["approval_required_for_publish"] is True

    exam_id = result.data["exam_id"]

    # --------------------------------------------------------
    # STEP 2: The exam itself must be academically approved
    # before ExamEngine allows publication.
    # --------------------------------------------------------

    approved_exam = exams.approve(
        exam_id,
        "admin_1",
    )

    assert approved_exam.status == "approved"
    assert approved_exam.approved_by == "admin_1"

    # --------------------------------------------------------
    # STEP 3: Publishing is a separate high-impact agent task.
    # The task itself requires explicit approval.
    # --------------------------------------------------------

    publish_task = engine.create_task(
        "publish_exam",
        "teacher_1",
        {
            "exam_id": exam_id,
        },
    )

    assert publish_task.requires_approval is True

    try:
        engine.execute(publish_task.id)
        assert False
    except PermissionError as exc:
        assert str(exc) == "APPROVAL_REQUIRED_BEFORE_EXECUTION"

    # --------------------------------------------------------
    # STEP 4: Human approval unlocks the publish task.
    # --------------------------------------------------------

    engine.approve(
        publish_task.id,
        "admin_1",
    )

    published = engine.execute(
        publish_task.id
    )

    assert published.status == "completed"
    assert published.data["status"] == "published"

    # Final domain-state verification.
    assert exams.exams[exam_id].status == "published"


def test_learning_analytics_agent():
    engine = AcademicAgentEngine()

    analytics = AnalyticsService()
    assessments = AssessmentService()
    exams = ExamEngine(QuestionBank())

    exam = exams.generate(
        "Science Test",
        "Science",
        "Grade 8",
        60,
        [],
        100,
    )

    assessment = assessments.create(
        "student_1",
        exam.id,
        40,
        100,
    )

    workflow = AcademicWorkflow(
        engine,
        analytics_service=analytics,
    )

    workflow.register_default_agents()
    workflow.connect_handlers()

    task = engine.create_task(
        "analyze_progress",
        "teacher_1",
        {
            "student_id": "student_1",
            "assessments": [assessment],
            "topic_by_exam": {
                exam.id: "Science",
            },
        },
    )

    result = engine.execute(task.id)

    assert result.status == "completed"
    assert result.data["weak_topics"] == ["Science"]


def test_command_router():
    router = AcademicCommandRouter()

    result = router.route(
        "Generate an exam from the book"
    )

    assert result["action"] == "generate_exam"
    assert result["provider_independent"] is True


def test_learning_plan_model():
    plan = LearningPlan(
        student_id="student_1",
        goals=["Improve Mathematics"],
        weak_topics=["Algebra"],
    )

    assert plan.student_id == "student_1"
    assert "Algebra" in plan.weak_topics
