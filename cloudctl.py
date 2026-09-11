#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

ENGINE = Path(__file__).resolve().parent / "tools" / "cloud_host" / "cloudctl.py"

if not ENGINE.is_file():
    print("ERROR: Cloud engine not found:")
    print(ENGINE)
    raise SystemExit(1)

runpy.run_path(str(ENGINE), run_name="__main__")
