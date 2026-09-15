
from core.agents.engine.agent_engine import AgentEngine
from core.agents.engine.department_registry import DepartmentRegistry
from core.agents.knowledge.shared_knowledge import SharedKnowledgeBus
from core.agents.models.agent_models import KnowledgeItem


def test_agent_registration():
    engine = AgentEngine()

    agent = engine.register_agent(
        "Education Agent",
        "education",
        ["analyze_book", "create_exam"],
    )

    assert agent.agent_id in engine.agents
    assert agent.department == "education"
    assert "create_exam" in agent.capabilities


def test_task_assignment_and_execution():
    engine = AgentEngine()

    agent = engine.register_agent(
        "Education Agent",
        "education",
        ["analyze_book"],
    )

    engine.register_handler(
        "analyze_book",
        lambda payload: {
            "analyzed": True,
            "input": payload,
        },
    )

    task = engine.create_task(
        "Analyze textbook",
        "education",
    )

    engine.assign_task(
        task.task_id,
        agent.agent_id,
    )

    result = engine.execute(
        task.task_id,
        "analyze_book",
        {"book": "sample"},
    )

    assert result["executed"] is True
    assert result["status"] == "completed"
    assert result["evidence"]["execution_confirmed"] is True


def test_approval_gate():
    engine = AgentEngine()

    agent = engine.register_agent(
        "Finance Agent",
        "finance",
        ["ledger_action"],
    )

    engine.register_handler(
        "ledger_action",
        lambda payload: "executed",
    )

    task = engine.create_task(
        "Sensitive ledger operation",
        "finance",
        approval_required=True,
    )

    engine.assign_task(
        task.task_id,
        agent.agent_id,
    )

    result = engine.execute(
        task.task_id,
        "ledger_action",
    )

    assert result["executed"] is False
    assert result["status"] == "awaiting_approval"

    result = engine.execute(
        task.task_id,
        "ledger_action",
        approval_granted=True,
    )

    assert result["executed"] is True


def test_delegation():
    engine = AgentEngine()

    agent = engine.register_agent(
        "Education Agent",
        "education",
        ["research"],
    )

    task = engine.create_task(
        "Research education system",
        "education",
    )

    engine.assign_task(
        task.task_id,
        agent.agent_id,
    )

    child = engine.delegate(
        task.task_id,
        "islamic_research",
    )

    assert child.department == "islamic_research"
    assert child.requested_by == agent.agent_id


def test_knowledge_bus():
    bus = SharedKnowledgeBus()

    item = KnowledgeItem(
        knowledge_id="k1",
        topic="education",
        content={"fact": "verified test"},
        source="test",
        verified=True,
        confidence=0.95,
    )

    bus.publish(item)

    assert bus.count() == 1
    assert len(bus.search("education")) == 1
    assert len(bus.search("education", verified_only=True)) == 1


def test_department_registry():
    registry = DepartmentRegistry()

    registry.register(
        "education",
        "Education department",
    )

    registry.register(
        "finance",
        "Finance department",
    )

    registry.disable("finance")

    assert registry.get("education")["enabled"] is True
    assert registry.get("finance")["enabled"] is False
    assert len(registry.list_enabled()) == 1
