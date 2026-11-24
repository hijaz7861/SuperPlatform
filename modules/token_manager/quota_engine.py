"""Daily/weekly token quota with auto-recharge."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta


class QuotaEngine:
    def __init__(self, daily_limit=10000, recharge_hours=24, state_dir=None):
        self.daily_limit = daily_limit
        self.recharge_hours = recharge_hours
        self.state_dir = Path(state_dir) if state_dir else Path(".superplatform/token_state")
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _state_path(self, user_id):
        return self.state_dir / f"{user_id}.json"

    def _load(self, user_id):
        p = self._state_path(user_id)
        if p.exists():
            return json.loads(p.read_text())
        now = datetime.now(timezone.utc)
        state = {"user_id": user_id, "remaining": self.daily_limit, "last_recharge": now.isoformat(), "total_consumed": 0}
        self._save(user_id, state)
        return state

    def _save(self, user_id, state):
        self._state_path(user_id).write_text(json.dumps(state, indent=2))

    def get_remaining(self, user_id):
        state = self._load(user_id)
        if self._should_recharge(state):
            state["remaining"] = self.daily_limit
            state["last_recharge"] = datetime.now(timezone.utc).isoformat()
            self._save(user_id, state)
        return state["remaining"]

    def _should_recharge(self, state):
        last = datetime.fromisoformat(state["last_recharge"])
        return datetime.now(timezone.utc) - last >= timedelta(hours=self.recharge_hours)

    def consume(self, user_id, tokens):
        state = self._load(user_id)
        if self._should_recharge(state):
            state["remaining"] = self.daily_limit
            state["last_recharge"] = datetime.now(timezone.utc).isoformat()
        if tokens > state["remaining"]:
            self._save(user_id, state)
            return False
        state["remaining"] -= tokens
        state["total_consumed"] += tokens
        self._save(user_id, state)
        return True
