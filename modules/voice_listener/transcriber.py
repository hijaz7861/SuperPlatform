"""Speech-to-text transcriber with multiple backends."""
import os

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import whisper
except ImportError:
    whisper = None


class Transcriber:
    def __init__(self, backend="auto"):
        self.backend = backend
        self.recognizer = sr.Recognizer() if sr else None

    def transcribe_file(self, audio_path):
        if sr and self.recognizer:
            try:
                with sr.AudioFile(audio_path) as source:
                    audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio)
            except Exception as e:
                return f"[error: {e}]"
        if whisper:
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            return result.get("text", "")
        return "[no STT backend available - mock transcript]"

    def transcribe_microphone(self, timeout=5):
        if not sr or not self.recognizer:
            return "[no microphone backend available]"
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            return self.recognizer.recognize_google(audio)
        except Exception as e:
            return f"[error: {e}]"
