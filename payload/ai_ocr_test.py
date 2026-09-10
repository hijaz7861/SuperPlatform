#!/usr/bin/env python3

from pathlib import Path
import sys

ROOT = Path.home() / "SuperPlatform"

required = [
    ROOT / "agent",
    ROOT / "modules" / "ai",
    ROOT / "modules" / "ocr",
]

print("=== AI / AGENT / OCR INTEGRITY TEST ===")

failed = 0

for path in required:
    if path.is_dir():
        print(f"PASS: {path.relative_to(ROOT)}")
    else:
        print(f"FAIL: {path.relative_to(ROOT)}")
        failed += 1

print(f"Python: {sys.version.split()[0]}")

if failed == 0:
    print("AI/AGENT/OCR INTEGRITY: PASS")
    sys.exit(0)
else:
    print(f"AI/AGENT/OCR INTEGRITY: FAIL ({failed})")
    sys.exit(1)
