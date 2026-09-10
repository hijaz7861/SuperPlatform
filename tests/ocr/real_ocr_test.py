import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont
from modules.ocr.real_ocr import RealOCREngine


TEST_IMAGE = ROOT / "tests" / "ocr" / "test_text.png"

EXPECTED = "HIJAZ COIN 12345"


def create_test_image():
    image = Image.new("RGB", (1200, 300), "white")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(
            "/system/fonts/Roboto-Regular.ttf",
            80
        )
    except Exception:
        font = ImageFont.load_default()

    draw.text(
        (50, 90),
        EXPECTED,
        fill="black",
        font=font
    )

    image.save(TEST_IMAGE)


def main():
    engine = RealOCREngine()

    assert engine.available(), "Tesseract is not available"

    create_test_image()

    print("TEST IMAGE: CREATED")

    extracted = engine.extract(TEST_IMAGE)

    print("OCR OUTPUT:")
    print(extracted)

    normalized = " ".join(extracted.upper().split())
    expected = " ".join(EXPECTED.upper().split())

    if normalized == expected:
        print("EXACT OCR MATCH: PASS")
    elif expected in normalized:
        print("OCR CONTENT MATCH: PASS")
    else:
        print("OCR CONTENT MATCH: FAIL")
        print("EXPECTED:", expected)
        print("ACTUAL:", normalized)
        raise SystemExit(1)

    print("REAL OCR ENGINE: PASS")


if __name__ == "__main__":
    main()
