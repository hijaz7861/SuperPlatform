"""Track token usage per user."""
import json
from pathlib import Path
from datetime import datetime, timezone


class UsageTracker:
    def __init__(self, log_dir=None):
        self.log_dir = Path(log_dir) if log_dir else Path(".superplatform/usage_logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, user_id, tokens, endpoint, latency_ms=None):
        entry = {
            "user_id": user_id,
            "tokens": tokens,
            "endpoint": endpoint,
            "latency_ms": latency_ms,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        log_file = self.log_dir / f"{datetime.now(timezone.utc).date()}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def get_daily_usage(self, date=None):
        date = date or datetime.now(timezone.utc).date()
        log_file = self.log_dir / f"{date}.jsonl"
        if not log_file.exists():
            return []
        return [json.loads(line) for line in log_file.read_text().splitlines() if line.strip()]
