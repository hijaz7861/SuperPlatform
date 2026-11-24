"""Parse natural language chat into structured intents."""
import re

INTENTS = {
    "scan_problems": ["scan", "find problems", "search problems", "problem scan"],
    "solve": ["solve", "fix", "resolve", "answer"],
    "price": ["price", "charge", "cost", "how much", "quote"],
    "outreach": ["contact", "email", "message", "reach out", "dm"],
    "status": ["status", "health", "report", "progress"],
    "voice": ["listen", "voice", "speak", "audio"],
    "token": ["token", "quota", "limit", "recharge"],
    "help": ["help", "commands", "what can you do"],
}


class IntentParser:
    def parse(self, text):
        text_l = text.lower().strip()
        for intent, keywords in INTENTS.items():
            for kw in keywords:
                if kw in text_l:
                    return {"intent": intent, "raw": text, "keyword": kw}
        return {"intent": "unknown", "raw": text, "keyword": None}

    def extract_params(self, text):
        # Extract simple key:value or quoted strings
        params = {}
        m = re.search(r"subreddit[:\s]+(\w+)", text, re.I)
        if m:
            params["subreddit"] = m.group(1)
        m = re.search(r"limit[:\s]+(\d+)", text, re.I)
        if m:
            params["limit"] = int(m.group(1))
        m = re.search(r"amount[:\s]+(\d+)", text, re.I)
        if m:
            params["amount"] = int(m.group(1))
        return params
