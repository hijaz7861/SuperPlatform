"""Aggregate results from distributed workers."""
class Aggregator:
    def __init__(self):
        self.results = []

    def add(self, result):
        self.results.append(result)

    def summary(self):
        ok = [r for r in self.results if r.get("ok")]
        fail = [r for r in self.results if not r.get("ok")]
        return {
            "total": len(self.results),
            "success": len(ok),
            "failed": len(fail),
            "workers_used": len(set(r.get("worker") for r in self.results)),
        }

    def all_results(self):
        return self.results
