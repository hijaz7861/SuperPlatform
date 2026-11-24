"""Conversation context memory."""
from collections import deque


class ContextMemory:
    def __init__(self, max_turns=20):
        self.turns = deque(maxlen=max_turns)
        self.state = {}

    def add(self, role, text, intent=None):
        self.turns.append({"role": role, "text": text, "intent": intent})

    def get_recent(self, n=5):
        return list(self.turns)[-n:]

    def set_state(self, key, value):
        self.state[key] = value

    def get_state(self, key, default=None):
        return self.state.get(key, default)

    def clear(self):
        self.turns.clear()
        self.state.clear()
