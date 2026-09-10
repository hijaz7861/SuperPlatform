#!/usr/bin/env python3
import json
import platform
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

def test():
    config = json.loads((BASE / "config.json").read_text())
    manifest = json.loads((BASE / "manifest.json").read_text())

    assert config["mode"] == "development"
    assert config["auto_test"] is True
    assert config["security"]["allow_destructive_actions"] is False
    assert manifest["name"] == "SuperPlatform Payload"

    print("=== SUPERPLATFORM PAYLOAD TEST ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.system()}")
    print("Manifest: PASS")
    print("Config: PASS")
    print("Safety defaults: PASS")
    print("PAYLOAD TEST: PASS")

if __name__ == "__main__":
    test()
