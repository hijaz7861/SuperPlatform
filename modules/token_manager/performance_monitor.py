"""Performance monitoring for free-tier usage."""
import statistics
from collections import defaultdict


class PerformanceMonitor:
    def __init__(self):
        self.latencies = defaultdict(list)
        self.errors = defaultdict(int)
        self.requests = defaultdict(int)

    def record(self, endpoint, latency_ms, success=True):
        self.latencies[endpoint].append(latency_ms)
        self.requests[endpoint] += 1
        if not success:
            self.errors[endpoint] += 1

    def report(self, endpoint=None):
        endpoints = [endpoint] if endpoint else list(self.latencies.keys())
        result = {}
        for ep in endpoints:
            lats = self.latencies.get(ep, [])
            reqs = self.requests.get(ep, 0)
            errs = self.errors.get(ep, 0)
            result[ep] = {
                "requests": reqs,
                "errors": errs,
                "error_rate": round(errs / reqs, 4) if reqs else 0,
                "p50_ms": round(statistics.median(lats), 2) if lats else 0,
                "p95_ms": round(sorted(lats)[int(len(lats) * 0.95)] if lats else 0, 2),
                "avg_ms": round(statistics.mean(lats), 2) if lats else 0,
            }
        return result
