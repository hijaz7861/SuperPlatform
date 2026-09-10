#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path.home() / "SuperPlatform"

sys.path.insert(0, str(ROOT))

from modules.ai.engine import AIEngine
from modules.ocr.engine import OCREngine


def main():

    print("=== AI ENGINE ===")

    ai = AIEngine()

    health = ai.health()

    assert health["status"] == "ok"

    result = ai.process(
        "SuperPlatform AI engine local smoke test"
    )

    assert result["words"] == 6
    assert result["length"] > 0

    print("AI import: PASS")
    print("AI health: PASS")
    print("AI processing: PASS")


    print()
    print("=== OCR ENGINE ===")

    ocr = OCREngine()

    health = ocr.health()

    assert health["status"] == "ok"

    result = ocr.extract_text(
        "SuperPlatform OCR smoke test"
    )

    assert result["words"] == 4
    assert result["characters"] > 0

    print("OCR import: PASS")
    print("OCR health: PASS")
    print("OCR text extraction: PASS")


    print()
    print("=== ENGINE SUMMARY ===")
    print("AI ENGINE: PASS")
    print("OCR ENGINE: PASS")
    print("AI/OCR ENGINE SMOKE TEST: PASS")


if __name__ == "__main__":
    main()
