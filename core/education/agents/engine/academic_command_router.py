class AcademicCommandRouter:
    """
    Deterministic command-routing foundation.

    It intentionally does not claim full NLP/LLM capability.
    An AI provider can be attached later without changing
    the academic workflow contract.
    """

    COMMANDS = {
        "exam": "generate_exam",
        "test": "generate_exam",
        "book": "analyze_book",
        "analyze": "analyze_book",
        "progress": "analyze_progress",
        "performance": "analyze_progress",
    }

    def route(self, command: str):
        text = command.strip().lower()

        for keyword, action in self.COMMANDS.items():
            if keyword in text:
                return {
                    "action": action,
                    "confidence": 1.0,
                    "provider_independent": True,
                }

        return {
            "action": "unknown",
            "confidence": 0.0,
            "provider_independent": True,
        }
