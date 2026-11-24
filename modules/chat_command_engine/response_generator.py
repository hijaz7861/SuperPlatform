"""Generate human-friendly responses."""
TEMPLATES = {
    "scan_problems": "Scanning {subreddit} for problems... Found {count} issues.",
    "solve": "Solution drafted: {solution}",
    "price": "Proposed charge: ${amount}",
    "outreach": "Outreach drafted and ready to send.",
    "status": "System status: {status}",
    "token": "Token quota: {remaining} remaining.",
    "voice": "Voice listener: {status}",
    "help": "Available commands: scan, solve, price, outreach, status, token, voice, help",
    "unknown": "I didn't understand that. Type 'help' for available commands.",
}


class ResponseGenerator:
    def generate(self, intent, data=None):
        data = data or {}
        tpl = TEMPLATES.get(intent, TEMPLATES["unknown"])
        try:
            return tpl.format(**data)
        except KeyError:
            return tpl
