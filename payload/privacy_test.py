import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.privacy.core import PrivacyEngine

engine = PrivacyEngine()

h = engine.hash_identifier("test-user")

assert len(h) == 64
assert h != "test-user"

result = engine.redact(
    "email test@example.com number 03001234567"
)

assert "test@example.com" not in result
assert "03001234567" not in result
assert "[REDACTED_EMAIL]" in result
assert "[REDACTED_NUMBER]" in result

print("HASH TEST: PASS")
print("REDACTION TEST: PASS")
print("PRIVACY ENGINE: PASS")
