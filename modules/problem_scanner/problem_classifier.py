"""Classify problems into categories for solution matching."""
import re


class ProblemClassifier:
    CATEGORIES = {
        "code_bug": ["error", "bug", "exception", "traceback", "not working", "crash"],
        "code_request": ["write code", "implement", "build", "create", "develop"],
        "tech_support": ["install", "setup", "configure", "wifi", "network", "driver"],
        "design": ["design", "ui", "ux", "logo", "layout", "css"],
        "data": ["data", "csv", "excel", "database", "sql", "pandas"],
        "general": [],
    }

    def classify(self, problem):
        text = (problem.get("title", "") + " " + problem.get("body", "")).lower()
        scores = {}
        for cat, keywords in self.CATEGORIES.items():
            scores[cat] = sum(1 for kw in keywords if kw in text)
        best = max(scores, key=scores.get)
        if scores[best] == 0:
            best = "general"
        return best

    def classify_batch(self, problems):
        for p in problems:
            p["category"] = self.classify(p)
        return problems
