
from ..models.guidance_expansion_models import GuidanceCase


class GuidanceExpansionEngine:

    def __init__(self):
        self.cases = {}

    def create_case(self, case_id, topic):
        case = GuidanceCase(case_id, topic)
        self.cases[case_id] = case
        return case

    def attach_evidence(self, case, evidence_id):
        case.evidence_ids.append(evidence_id)
        return case

    def finalize(self, case, human_approved=False):
        if not human_approved:
            case.status = "REVIEW_REQUIRED"
            return case

        case.status = "APPROVED_WITH_HUMAN_REVIEW"
        return case
