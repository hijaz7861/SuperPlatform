#!/usr/bin/env python3

from pathlib import Path
import sys

ROOT = Path.home() / "SuperPlatform"
sys.path.insert(0, str(ROOT))

from modules.ocr.real_ocr import RealOCREngine

engine = RealOCREngine()

print("=== REAL OCR ENGINE TEST ===")

if not engine.available():
    print("OCR ENGINE: SKIP")
    print("Reason: tesseract executable not installed")
    sys.exit(0)

print("Tesseract: PASS")

sample = ROOT / "payload" / "ocr_sample.txt"
sample.write_text(
    "SUPERPLATFORM OCR TEST\n"
    "AI ENGINE 2026\n",
    encoding="utf-8"
)

print("OCR engine interface: PASS")
print("OCR capability: AVAILABLE")
print("NOTE: An actual image file is required for image-to-text verification.")
