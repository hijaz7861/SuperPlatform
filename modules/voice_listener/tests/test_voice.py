import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.voice_listener.wake_word import WakeWordDetector
from modules.voice_listener.transcriber import Transcriber
from modules.voice_listener.listener import VoiceListener


def test_wake_word():
    wd = WakeWordDetector()
    det, word = wd.detect("hey platform scan problems")
    assert det is True


def test_transcriber_mock():
    t = Transcriber()
    # No backend -> returns mock/error string, not crash
    out = t.transcribe_file("/nonexistent.wav")
    assert isinstance(out, str)


def test_listener_process():
    vl = VoiceListener()
    r = vl.process_audio_file("/nonexistent.wav")
    assert "transcript" in r


if __name__ == "__main__":
    test_wake_word()
    test_transcriber_mock()
    test_listener_process()
    print("VOICE LISTENER TESTS: PASS")
