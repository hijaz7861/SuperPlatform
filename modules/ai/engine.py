#!/usr/bin/env python3

class AIEngine:
    name = "SuperPlatform Local AI Engine"
    version = "0.1.0"

    def health(self):
        return {
            "engine": self.name,
            "version": self.version,
            "status": "ok"
        }

    def process(self, text):
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        cleaned = " ".join(text.split())

        return {
            "input": text,
            "cleaned": cleaned,
            "length": len(cleaned),
            "words": len(cleaned.split()) if cleaned else 0
        }
