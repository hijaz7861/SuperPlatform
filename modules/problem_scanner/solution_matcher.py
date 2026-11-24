"""Match problems to solution templates."""
import json
from pathlib import Path


class SolutionMatcher:
    def __init__(self, templates_path=None):
        self.templates = {}
        if templates_path and Path(templates_path).exists():
            self.templates = json.loads(Path(templates_path).read_text())

    def match(self, problem):
        category = problem.get("category", "general")
        template = self.templates.get(category, self.templates.get("general", {}))
        return {
            "problem_id": problem.get("id"),
            "category": category,
            "solution_template": template.get("template", "We can help solve this."),
            "estimated_hours": template.get("hours", 2),
            "confidence": 0.7,
        }

    def match_batch(self, problems):
        return [self.match(p) for p in problems]
