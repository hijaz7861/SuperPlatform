"""Route parsed intents to module handlers."""
from .intent_parser import IntentParser


class CommandRouter:
    def __init__(self):
        self.handlers = {}
        self.parser = IntentParser()

    def register(self, intent, handler):
        self.handlers[intent] = handler

    def route(self, text):
        parsed = self.parser.parse(text)
        params = self.parser.extract_params(text)
        intent = parsed["intent"]
        handler = self.handlers.get(intent)
        if handler:
            return {"intent": intent, "params": params, "result": handler(params, parsed)}
        return {"intent": intent, "params": params, "result": f"No handler for '{intent}'"}
