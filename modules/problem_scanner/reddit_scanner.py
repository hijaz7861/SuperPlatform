"""Reddit problem scanner using PRAW (read-only, public data)."""
import json
from pathlib import Path
from datetime import datetime, timezone

try:
    import praw
except ImportError:
    praw = None


class RedditScanner:
    def __init__(self, client_id=None, client_secret=None, user_agent="SuperPlatform/1.0"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = None
        if praw and client_id and client_secret:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
            )

    def scan_subreddit(self, subreddit_name, limit=25, sort="new"):
        """Scan a subreddit for problem posts. Returns list of problem dicts."""
        results = []
        if not self.reddit:
            # Offline/mock mode for testing without credentials
            return self._mock_scan(subreddit_name, limit)
        sub = self.reddit.subreddit(subreddit_name)
        for post in getattr(sub, sort)(limit=limit):
            results.append({
                "id": post.id,
                "title": post.title,
                "body": post.selftext or "",
                "author": str(post.author) if post.author else "[deleted]",
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat(),
                "url": f"https://reddit.com{post.permalink}",
                "subreddit": subreddit_name,
            })
        return results

    def _mock_scan(self, subreddit_name, limit):
        """Mock data for offline testing."""
        return [
            {
                "id": f"mock_{i}",
                "title": f"Sample problem {i} in {subreddit_name}",
                "body": "I need help with this issue. Can someone solve it?",
                "author": f"user_{i}",
                "score": 5,
                "num_comments": 2,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "url": f"https://reddit.com/r/{subreddit_name}/mock_{i}",
                "subreddit": subreddit_name,
            }
            for i in range(min(limit, 3))
        ]

    def scan_multiple(self, subreddits, limit=25):
        all_results = []
        for sr in subreddits:
            all_results.extend(self.scan_subreddit(sr, limit=limit))
        return all_results
