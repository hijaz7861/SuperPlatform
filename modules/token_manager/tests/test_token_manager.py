"""Tests for token manager module."""
import sys, tempfile, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.token_manager.quota_engine import QuotaEngine
from modules.token_manager.rate_limiter import RateLimiter
from modules.token_manager.usage_tracker import UsageTracker
from modules.token_manager.performance_monitor import PerformanceMonitor


def test_quota_consume_and_recharge():
    with tempfile.TemporaryDirectory() as d:
        qe = QuotaEngine(daily_limit=10, recharge_hours=24, state_dir=d)
        assert qe.consume("u1", 5) is True
        assert qe.get_remaining("u1") == 5
        assert qe.consume("u1", 10) is False
        assert qe.get_remaining("u1") == 5


def test_rate_limiter():
    rl = RateLimiter(max_per_minute=2)
    assert rl.allow_minute("k1") is True
    assert rl.allow_minute("k1") is True
    assert rl.allow_minute("k1") is False


def test_usage_tracker():
    with tempfile.TemporaryDirectory() as d:
        ut = UsageTracker(log_dir=d)
        e = ut.log("u1", 5, "/api/test", latency_ms=120)
        assert e["tokens"] == 5
        logs = ut.get_daily_usage()
        assert len(logs) == 1


def test_performance_monitor():
    pm = PerformanceMonitor()
    pm.record("/api", 100, True)
    pm.record("/api", 200, True)
    r = pm.report("/api")
    assert r["/api"]["requests"] == 2
    assert r["/api"]["p50_ms"] >= 100


if __name__ == "__main__":
    test_quota_consume_and_recharge()
    test_rate_limiter()
    test_usage_tracker()
    test_performance_monitor()
    print("TOKEN MANAGER TESTS: PASS")
