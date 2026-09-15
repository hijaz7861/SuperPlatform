
from typing import Any, Dict, List
from uuid import uuid4

from core.islamic.models.islamic_models import (
    ResearchQuestion,
    EvidenceItem,
    GuidanceResult,
)
from core.islamic.knowledge.knowledge_registry import (
    IslamicKnowledgeRegistry,
)


class IslamicResearchEngine:

    ALLOWED_STATUSES = {
        "research_only",
        "evidence_found",
        "needs_verification",
        "needs_human_review",
        "guidance_ready",
        "disagreement_detected",
    }

    def __init__(self, knowledge_registry=None):
        self.knowledge = (
            knowledge_registry
            or IslamicKnowledgeRegistry()
        )

        self.questions: Dict[str, ResearchQuestion] = {}
        self.results: Dict[str, GuidanceResult] = {}
        self.audit_log: List[Dict[str, Any]] = []

    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    def create_question(
        self,
        question: str,
        category: str = "general",
        requested_by: str = "user",
    ):

        if not question or not question.strip():
            raise ValueError("Research question required")

        item = ResearchQuestion(
            question_id=str(uuid4()),
            question=question.strip(),
            category=category,
            requested_by=requested_by,
        )

        self.questions[item.question_id] = item

        self._audit(
            "question_created",
            item.question_id,
        )

        return item

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    def collect_evidence(
        self,
        question_id: str,
    ) -> List[EvidenceItem]:

        if question_id not in self.questions:
            raise KeyError(question_id)

        question = self.questions[question_id]

        results = self.knowledge.search(question.question)

        if not results:
            # Basic token matching fallback.
            words = [
                x.lower()
                for x in question.question.split()
                if len(x) >= 4
            ]

            found = []

            for item in self.knowledge.evidence.values():
                haystack = (
                    item.excerpt + " "
                    + item.source.title + " "
                    + item.source.locator
                ).lower()

                if any(word in haystack for word in words):
                    found.append(item)

            results = found

        self._audit(
            "evidence_collected",
            question_id,
            {"count": len(results)},
        )

        return results

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    def verify_evidence(
        self,
        evidence_id: str,
        method: str,
        verified: bool,
    ):

        item = self.knowledge.get_evidence(evidence_id)

        if item is None:
            raise KeyError(evidence_id)

        if not method:
            raise ValueError(
                "Verification method required"
            )

        item.verified = bool(verified)
        item.verification_method = method

        self._audit(
            "evidence_verification",
            evidence_id,
            {
                "verified": item.verified,
                "method": method,
            },
        )

        return item

    # --------------------------------------------------------
    # GUIDANCE SAFETY
    # --------------------------------------------------------

    def build_guidance(
        self,
        question_id: str,
        answer: str,
        evidence: List[EvidenceItem],
        confidence: float,
        disagreement: bool = False,
        notes=None,
    ):

        if question_id not in self.questions:
            raise KeyError(question_id)

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Confidence must be between 0 and 1"
            )

        evidence = evidence or []
        notes = notes or []

        verified_count = sum(
            item.verified
            for item in evidence
        )

        # ----------------------------------------------------
        # IMPORTANT:
        # Software confidence does NOT mean religious certainty.
        # Human review remains mandatory for guidance.
        # ----------------------------------------------------

        if disagreement:
            status = "disagreement_detected"
            requires_review = True

        elif not evidence:
            status = "research_only"
            requires_review = True

        elif verified_count < len(evidence):
            status = "needs_verification"
            requires_review = True

        else:
            status = "needs_human_review"
            requires_review = True

        result = GuidanceResult(
            result_id=str(uuid4()),
            question_id=question_id,
            status=status,
            answer=answer,
            evidence=evidence,
            confidence=confidence,
            requires_human_review=requires_review,
            disagreement=disagreement,
            notes=notes,
        )

        self.results[result.result_id] = result

        self._audit(
            "guidance_built",
            result.result_id,
            {
                "status": status,
                "evidence_count": len(evidence),
                "verified_count": verified_count,
                "human_review": requires_review,
            },
        )

        return result

    # --------------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------------

    def approve_guidance(
        self,
        result_id: str,
        reviewer: str,
        review_note: str = "",
    ):

        if not reviewer:
            raise ValueError("Reviewer required")

        result = self.results[result_id]

        if result.status == "research_only":
            raise RuntimeError(
                "Cannot approve guidance without evidence"
            )

        if result.status == "needs_verification":
            raise RuntimeError(
                "Evidence verification incomplete"
            )

        # Explicit human approval.
        result.requires_human_review = False
        result.status = "guidance_ready"

        result.notes.append(
            f"Human review by {reviewer}: {review_note}"
        )

        self._audit(
            "guidance_human_approved",
            result_id,
            {"reviewer": reviewer},
        )

        return result

    # --------------------------------------------------------
    # AUDIT
    # --------------------------------------------------------

    def _audit(self, event, target, details=None):
        from datetime import datetime, timezone

        self.audit_log.append({
            "event": event,
            "target": target,
            "details": details or {},
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        })

    def health(self):
        return {
            "questions": len(self.questions),
            "results": len(self.results),
            "sources": len(self.knowledge.sources),
            "evidence": len(self.knowledge.evidence),
            "audit_events": len(self.audit_log),
        }
