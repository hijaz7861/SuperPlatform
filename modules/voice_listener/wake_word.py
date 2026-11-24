"""Wake word detection (lightweight keyword match)."""
class WakeWordDetector:
    def __init__(self, wake_words=None):
        self.wake_words = wake_words or ["hey platform", "super platform", "listen"]

    def detect(self, text):
        text_l = text.lower()
        for w in self.wake_words:
            if w in text_l:
                return True, w
        return False, None
