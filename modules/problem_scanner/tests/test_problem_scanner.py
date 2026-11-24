"""Tests for problem scanner module."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.problem_scanner.reddit_scanner import RedditScanner
from modules.problem_scanner.problem_classifier import ProblemClassifier
from modules.problem_scanner.pricing_engine import PricingEngine
from modules.problem_scanner.solution_matcher import SolutionMatcher
from modules.problem_scanner.outreach_drafter import OutreachDrafter


def test_reddit_mock_scan():
    s = RedditScanner()
    posts = s.scan_subreddit("techsupport", limit=2)
    assert len(posts) == 2
    assert "title" in posts[0]


def test_classifier():
    c = ProblemClassifier()
    p = {"title": "Python error traceback crash", "body": ""}
    assert c.classify(p) == "code_bug"


def test_pricing():
    pe = PricingEngine()
    problem = {"category": "code_bug"}
    solution = {"estimated_hours": 2}
    r = pe.calculate(problem, solution)
    assert r["amount"] == 50
    assert r["currency"] == "USD"


def test_outreach_draft():
    od = OutreachDrafter()
    problem = {"title": "Need help", "author": "user1"}
    solution = {"solution_template": "We can fix it.", "estimated_hours": 1}
    pricing = {"amount": 25}
    email = od.draft_email(problem, solution, pricing)
    assert "subject" in email
    assert "25" in email["body"]


def test_solution_matcher():
    sm = SolutionMatcher()
    problem = {"id": "1", "category": "general"}
    m = sm.match(problem)
    assert m["problem_id"] == "1"


if __name__ == "__main__":
    test_reddit_mock_scan()
    test_classifier()
    test_pricing()
    test_outreach_draft()
    test_solution_matcher()
    print("PROBLEM SCANNER TESTS: PASS")
