"""High-level voice listener combining wake word + transcription + command routing."""
from .transcriber import Transcriber
from .wake_word import WakeWordDetector


class VoiceListener:
    def __init__(self, router=None, wake_words=None):
        self.transcriber = Transcriber()
        self.wake = WakeWordDetector(wake_words)
        self.router = router
        self.active = False

    def process_audio_file(self, audio_path):
        text = self.transcriber.transcribe_file(audio_path)
        detected, word = self.wake.detect(text)
        result = {"transcript": text, "wake_detected": detected, "wake_word": word}
        if detected and self.router:
            cmd = text.replace(word, "").strip() if word else text
            result["command_result"] = self.router.route(cmd)
        return result

    def listen_once(self, timeout=5):
        text = self.transcriber.transcribe_microphone(timeout=timeout)
        detected, word = self.wake.detect(text)
        result = {"transcript": text, "wake_detected": detected, "wake_word": word}
        if detected and self.router:
            cmd = text.replace(word, "").strip() if word else text
            result["command_result"] = self.router.route(cmd)
        return result
