from ..models.research_models import (
    ResearchQuestion,
    ResearchFinding,
    ResearchResult,
)


class ResearchEngine:

    def create_question(self, question_id, question):
        return ResearchQuestion(
            question_id=question_id,
            question=question,
        )

    def add_finding(
        self,
        result,
        source,
        claim,
        confidence,
        verified=False,
    ):
        finding = ResearchFinding(
            source=source,
            claim=claim,
            confidence=round(
                max(0.0, min(1.0, float(confidence))),
                6,
            ),
            verified=verified,
        )

        result.findings.append(finding)

        return finding

    def verify_finding(self, finding):
        finding.verified = True
        return finding

    def finalize(self, result):
        # TARGETED AIM 08 STATE-FLOW FIX
        # Finalization is based on the actual findings attached
        # to this research result.
        findings = getattr(result, 'findings', None)
        if findings is None:
            findings = getattr(result, 'finding_ids', None)

        if not findings:
            result.status = 'REVIEW_REQUIRED'
            return result

        all_verified = True
        for finding in findings:
            if isinstance(finding, str):
                all_verified = False
                break

            verified = getattr(finding, 'verified', None)
            if verified is None:
                verified = getattr(finding, 'is_verified', None)

            if verified is not True:
                all_verified = False
                break

        result.status = 'VERIFIED' if all_verified else 'REVIEW_REQUIRED'
        return result

    def create_result(self, question):
        return ResearchResult(
            question_id=question.question_id
        )
