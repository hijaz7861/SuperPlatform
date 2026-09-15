
from core.islamic.models.islamic_models import (
    SourceReference,
    EvidenceItem,
)
from core.islamic.knowledge.knowledge_registry import (
    IslamicKnowledgeRegistry,
)
from core.islamic.engine.islamic_research_engine import (
    IslamicResearchEngine,
)
from core.islamic.policies.guidance_policy import (
    IslamicGuidancePolicy,
)


def make_registry():
    registry = IslamicKnowledgeRegistry()

    source = SourceReference(
        source_id="test-quran",
        source_type="quran",
        title="Test Quran Source",
        locator="2:255",
        language="ar",
    )

    registry.register_source(source)

    evidence = EvidenceItem(
        evidence_id="e1",
        source=source,
        excerpt="test evidence about knowledge",
        relevance=0.95,
        verified=False,
    )

    registry.add_evidence(evidence)

    return registry


def test_source_and_evidence_registry():
    registry = make_registry()

    assert registry.counts()["sources"] == 1
    assert registry.counts()["evidence"] == 1
    assert registry.counts()["verified_evidence"] == 0


def test_research_question_and_evidence():
    registry = make_registry()
    engine = IslamicResearchEngine(registry)

    question = engine.create_question(
        "knowledge",
        category="general",
    )

    evidence = engine.collect_evidence(
        question.question_id
    )

    assert len(evidence) == 1
    assert evidence[0].evidence_id == "e1"


def test_evidence_verification():
    registry = make_registry()
    engine = IslamicResearchEngine(registry)

    item = engine.verify_evidence(
        "e1",
        method="test_manual_source_check",
        verified=True,
    )

    assert item.verified is True
    assert item.verification_method == \
        "test_manual_source_check"


def test_human_review_gate():
    registry = make_registry()
    engine = IslamicResearchEngine(registry)

    question = engine.create_question(
        "knowledge",
        category="general",
    )

    evidence = engine.collect_evidence(
        question.question_id
    )

    engine.verify_evidence(
        "e1",
        method="test_manual_source_check",
        verified=True,
    )

    result = engine.build_guidance(
        question.question_id,
        "Research result requiring scholarly review.",
        evidence,
        confidence=0.90,
    )

    assert result.status == "needs_human_review"
    assert result.requires_human_review is True

    approved = engine.approve_guidance(
        result.result_id,
        reviewer="test_reviewer",
        review_note="Reviewed for test.",
    )

    assert approved.status == "guidance_ready"
    assert approved.requires_human_review is False


def test_disagreement_gate():
    registry = make_registry()
    engine = IslamicResearchEngine(registry)

    question = engine.create_question(
        "knowledge",
        category="general",
    )

    evidence = engine.collect_evidence(
        question.question_id
    )

    result = engine.build_guidance(
        question.question_id,
        "Multiple scholarly views require comparison.",
        evidence,
        confidence=0.80,
        disagreement=True,
    )

    assert result.status == \
        "disagreement_detected"

    assert result.requires_human_review is True


def test_unverified_evidence_cannot_be_final_guidance():
    registry = make_registry()
    engine = IslamicResearchEngine(registry)

    question = engine.create_question(
        "knowledge",
        category="general",
    )

    evidence = engine.collect_evidence(
        question.question_id
    )

    result = engine.build_guidance(
        question.question_id,
        "Unverified research result.",
        evidence,
        confidence=0.50,
    )

    assert result.status == "needs_verification"
    assert result.requires_human_review is True

    try:
        engine.approve_guidance(
            result.result_id,
            reviewer="test_reviewer",
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError(
            "Unverified guidance was incorrectly approved"
        )


def test_sensitive_policy():
    policy = IslamicGuidancePolicy()

    result = policy.evaluate(
        category="fatwa",
        evidence_verified=True,
    )

    assert result["allowed_for_research"] is True
    assert result["human_review_required"] is True
    assert result["guidance_ready"] is False
