"""Unified workflow loop: voice/chat -> scan -> classify -> price -> outreach -> report."""
import sys, json, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from modules.integration_bootstrap import build_registry
from modules.problem_scanner.reddit_scanner import RedditScanner
from modules.problem_scanner.problem_classifier import ProblemClassifier
from modules.problem_scanner.solution_matcher import SolutionMatcher
from modules.problem_scanner.pricing_engine import PricingEngine
from modules.problem_scanner.outreach_drafter import OutreachDrafter
from modules.token_manager.quota_engine import QuotaEngine
from modules.token_manager.usage_tracker import UsageTracker
from modules.token_manager.performance_monitor import PerformanceMonitor
from modules.chat_command_engine.intent_parser import IntentParser
from modules.chat_command_engine.response_generator import ResponseGenerator
from modules.distributed_agent.coordinator import Coordinator
from modules.config_loader import load_config


class WorkflowLoop:
    def __init__(self):
        self.registry = build_registry()
        pcfg = load_config("problem_scanner", {"scan_limit": 5, "target_subreddits": ["techsupport"]})
        tcfg = load_config("token_manager", {"free_tier": {"daily_token_limit": 10000}})
        self.scanner = RedditScanner()
        self.scan_limit = pcfg.get("scan_limit", 5)
        self.classifier = ProblemClassifier()
        self.matcher = SolutionMatcher()
        self.pricer = PricingEngine()
        self.drafter = OutreachDrafter()
        daily = tcfg.get("free_tier", {}).get("daily_token_limit", 10000)
        self.quota = QuotaEngine(daily_limit=daily)
        self.tracker = UsageTracker()
        self.perf = PerformanceMonitor()
        self.intent = IntentParser()
        self.responder = ResponseGenerator()
        self.user_id = "default_user"
        self.num_workers = 10

    def run_cycle(self, subreddit="techsupport", limit=5):
        t0 = time.time()
        # 0. Distributed parallel search across N workers
        coord = Coordinator(num_workers=self.num_workers)
        search_tasks = [{"action": "scan", "subreddit": subreddit, "i": i} for i in range(self.scan_limit)]
        coord.submit_tasks(search_tasks)
        coord.run(timeout=10)
        # 1. Scan
        problems = self.scanner.scan_subreddit(subreddit, limit=self.scan_limit)
        # 2. Classify
        problems = self.classifier.classify_batch(problems)
        # 3. Match solutions
        solutions = self.matcher.match_batch(problems)
        # 4. Price
        pricings = self.pricer.calculate_batch(problems, solutions)
        # 5. Draft outreach
        drafts = []
        for p, s, pr in zip(problems, solutions, pricings):
            drafts.append(self.drafter.draft_email(p, s, pr))
        # 6. Token tracking
        tokens_used = len(problems) * 100
        ok = self.quota.consume(self.user_id, tokens_used)
        self.tracker.log(self.user_id, tokens_used, f"scan:{subreddit}", latency_ms=int((time.time()-t0)*1000))
        self.perf.record("workflow_cycle", int((time.time()-t0)*1000), success=ok)
        # 7. Report
        report = {
            "subreddit": subreddit,
            "problems_found": len(problems),
            "solutions_drafted": len(drafts),
            "tokens_used": tokens_used,
            "quota_ok": ok,
            "remaining_quota": self.quota.get_remaining(self.user_id),
            "latency_ms": int((time.time()-t0)*1000),
        }
        return report, drafts

    def run(self, cycles=1, subreddit="techsupport", limit=5):
        results = []
        for i in range(cycles):
            report, drafts = self.run_cycle(subreddit, limit)
            results.append({"cycle": i+1, "report": report, "drafts_count": len(drafts)})
            print(f"Cycle {i+1}: {report['problems_found']} problems, {report['solutions_drafted']} drafts, quota_ok={report['quota_ok']}")
        # Save report
        out = ROOT / ".superplatform" / "reports" / "workflow_loop_report.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, indent=2))
        print(f"Report saved: {out}")
        return results


if __name__ == "__main__":
    loop = WorkflowLoop()
    loop.run(cycles=1, subreddit="techsupport", limit=5)
