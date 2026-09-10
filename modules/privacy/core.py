import hashlib
import re

class PrivacyEngine:

    def hash_identifier(self, value):
        return hashlib.sha256(
            str(value).encode("utf-8")
        ).hexdigest()

    def redact(self, text):
        text = str(text)

        text = re.sub(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            '[REDACTED_EMAIL]',
            text
        )

        text = re.sub(
            r'\b\d{10,15}\b',
            '[REDACTED_NUMBER]',
            text
        )

        return text
