from pathlib import Path
import shutil
import subprocess


class RealOCREngine:

    def available(self):
        return shutil.which("tesseract") is not None

    def extract(self, image_path):
        image = Path(image_path)

        if not image.exists():
            raise FileNotFoundError(image)

        result = subprocess.run(
            ["tesseract", str(image), "stdout"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or "Tesseract OCR failed"
            )

        return result.stdout.strip()
