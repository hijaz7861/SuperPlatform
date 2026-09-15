
class IslamicGuidancePolicy:

    SENSITIVE_CATEGORIES = {
        "fatwa",
        "halal_haram",
        "marriage",
        "divorce",
        "inheritance",
        "finance",
        "oath",
        "criminal",
        "medical",
    }

    def evaluate(
        self,
        category: str,
        evidence_verified: bool,
        disagreement: bool = False,
    ):
        reasons = []

        if category in self.SENSITIVE_CATEGORIES:
            reasons.append(
                "Sensitive religious category requires human review."
            )

        if not evidence_verified:
            reasons.append(
                "Evidence has not been fully verified."
            )

        if disagreement:
            reasons.append(
                "Scholarly disagreement must be represented."
            )

        return {
            "allowed_for_research": True,
            "guidance_ready": (
                len(reasons) == 0
            ),
            "human_review_required": True,
            "reasons": reasons,
        }
