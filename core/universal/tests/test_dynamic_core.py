
from core.universal.engines.dynamic_option_engine import (
    UniversalDynamicOptionEngine
)
from core.universal.policies.policy_engine import (
    UniversalPolicyEngine,
    PolicyResult,
)
from core.universal.universal_registry import UniversalRegistry


def test_dynamic_options():
    engine = UniversalDynamicOptionEngine()

    engine.add_option(
        "dark_mode",
        "Dark Mode",
        "boolean",
        False,
    )

    assert "dark_mode" in engine.options
    assert engine.options["dark_mode"].enabled is True

    engine.disable_option("dark_mode")
    assert engine.options["dark_mode"].enabled is False

    engine.enable_option("dark_mode")
    assert engine.options["dark_mode"].enabled is True


def test_dynamic_fields_actions_workflows():
    engine = UniversalDynamicOptionEngine()

    engine.add_field(
        "student_id",
        "Student ID",
        "string",
        required=True,
    )

    engine.add_action(
        "approve_exam",
        "Approve Exam",
        approval_required=True,
    )

    engine.add_workflow(
        "exam_approval",
        "Exam Approval",
        steps=[
            {"action": "submit"},
            {"action": "review"},
            {"action": "approve"},
        ],
    )

    schema = engine.export_schema()

    assert "student_id" in schema["fields"]
    assert "approve_exam" in schema["actions"]
    assert "exam_approval" in schema["workflows"]


def test_version_and_rollback():
    engine = UniversalDynamicOptionEngine()

    initial_version = engine.version()

    engine.add_option(
        "temporary",
        "Temporary",
    )

    changed_version = engine.version()

    assert changed_version > initial_version
    assert "temporary" in engine.options

    engine.rollback(initial_version)

    assert "temporary" not in engine.options


def test_policy_engine():
    policies = UniversalPolicyEngine()

    policies.register(
        "safe",
        lambda **ctx: PolicyResult(
            allowed=True,
            reason="Allowed",
        ),
    )

    result = policies.evaluate("safe")

    assert result.allowed is True


def test_registry():
    registry = UniversalRegistry()

    engine = UniversalDynamicOptionEngine()

    registry.register_engine(
        "dynamic_options",
        engine,
    )

    assert registry.get_engine("dynamic_options") is engine
