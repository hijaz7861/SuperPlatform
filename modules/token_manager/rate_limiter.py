"""Rate limiter using token bucket."""
import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_per_minute=20, max_per_hour=200):
        self.max_per_minute = max_per_minute
        self.max_per_hour = max_per_hour
        self._buckets = defaultdict(list)

    def _clean(self, key, window_sec):
        now = time.time()
        self._buckets[key] = [t for t in self._buckets[key] if now - t < window_sec]

    def allow(self, key, window_sec=60, limit=None):
        limit = limit or self.max_per_minute
        self._clean(key, window_sec)
        if len(self._buckets[key]) >= limit:
            return False
        self._buckets[key].append(time.time())
        return True

    def allow_minute(self, key):
        return self.allow(key, 60, self.max_per_minute)

    def allow_hour(self, key):
        return self.allow(key, 3600, self.max_per_hour)
