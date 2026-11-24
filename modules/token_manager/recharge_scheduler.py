"""Auto-recharge scheduler for free-tier tokens."""
import threading
import time
from datetime import datetime, timezone


class RechargeScheduler:
    def __init__(self, quota_engine, interval_hours=24, check_interval_sec=3600):
        self.quota_engine = quota_engine
        self.interval_hours = interval_hours
        self.check_interval_sec = check_interval_sec
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            # Recharge happens lazily in QuotaEngine.get_remaining/consume
            time.sleep(self.check_interval_sec)

    def force_recharge_all(self, user_ids):
        for uid in user_ids:
            state_path = self.quota_engine._state_path(uid)
            if state_path.exists():
                import json
                state = json.loads(state_path.read_text())
                state["remaining"] = self.quota_engine.daily_limit
                state["last_recharge"] = datetime.now(timezone.utc).isoformat()
                state_path.write_text(json.dumps(state, indent=2))
        return len(user_ids)
