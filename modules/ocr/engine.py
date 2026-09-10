#!/usr/bin/env python3

class OCREngine:
    name = "SuperPlatform Local OCR Engine"
    version = "0.1.0"

    def health(self):
        return {
            "engine": self.name,
            "version": self.version,
            "status": "ok"
        }

    def extract_text(self, text):
        if not isinstance(text, str):
            raise TypeError("OCR input must be a string")

        # Smoke-test adapter:
        # real image OCR can be connected later.
        return {
            "text": text,
            "characters": len(text),
            "words": len(text.split()) if text else 0
        }
