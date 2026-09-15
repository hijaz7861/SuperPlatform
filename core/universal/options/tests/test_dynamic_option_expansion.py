from core.universal.options.engine.dynamic_option_expansion_engine import (
    DynamicOptionExpansionEngine,
)
from core.universal.options.policies.option_expansion_policy import (
    OptionExpansionPolicy,
)


def test_add_update_enable_disable():
    engine = DynamicOptionExpansionEngine()

    option = engine.add_option(
        "attendance.mode",
        "Attendance Mode",
        value_type="enum",
        default="manual",
    )

    assert option.option_id == "attendance.mode"
    assert option.enabled is True

    engine.update_option(
        "attendance.mode",
        default="ai",
    )

    assert engine.get_option(
        "attendance.mode"
    ).default == "ai"

    engine.disable_option("attendance.mode")
    assert engine.get_option(
        "attendance.mode"
    ).enabled is False

    engine.enable_option("attendance.mode")
    assert engine.get_option(
        "attendance.mode"
    ).enabled is True


def test_versioning_and_rollback():
    engine = DynamicOptionExpansionEngine()

    engine.add_option(
        "exam.auto_generate",
        "Auto Generate Exam",
        value_type="boolean",
        default=False,
    )

    engine.update_option(
        "exam.auto_generate",
        default=True,
    )

    assert engine.get_option(
        "exam.auto_generate"
    ).version == 2

    engine.rollback(
        "exam.auto_generate",
        1,
    )

    option = engine.get_option(
        "exam.auto_generate"
    )

    assert option.default is False
    assert option.version == 1


def test_policy_validation():
    engine = DynamicOptionExpansionEngine()
    policy = OptionExpansionPolicy()

    option = engine.add_option(
        "teacher.ai",
        "Teacher AI",
    )

    assert policy.can_modify() is True
    assert policy.validate(option) is True


def test_audit_trail():
    engine = DynamicOptionExpansionEngine()

    engine.add_option(
        "student.analytics",
        "Student Analytics",
    )

    engine.update_option(
        "student.analytics",
        default=True,
    )

    engine.disable_option(
        "student.analytics",
    )

    actions = [
        item.action
        for item in engine.audit_log
    ]

    assert actions == [
        "ADD",
        "UPDATE",
        "DISABLE",
    ]
