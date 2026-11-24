"""Draft outreach emails/DMs for problem solutions."""
from datetime import datetime, timezone


class OutreachDrafter:
    def draft_email(self, problem, solution, pricing):
        subject = f"Solution for: {problem.get('title', 'your problem')}"
        body = (
            f"Hi {problem.get('author', 'there')},\n\n"
            f"I noticed your post: \"{problem.get('title', '')}\"\n\n"
            f"I can help solve this. {solution.get('solution_template', '')}\n\n"
            f"Estimated effort: {solution.get('estimated_hours', 2)} hours\n"
            f"Proposed charge: ${pricing.get('amount', 0)}\n\n"
            f"If interested, reply and we can start immediately.\n\n"
            f"Best regards,\nSuperPlatform Problem Solver\n"
            f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
        )
        return {"subject": subject, "body": body, "to": problem.get("author")}

    def draft_dm(self, problem, solution, pricing):
        return (
            f"Hi! I saw your problem: \"{problem.get('title', '')}\". "
            f"I can solve it for ${pricing.get('amount', 0)}. "
            f"Reply if interested!"
        )
