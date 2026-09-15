#!/usr/bin/env python3

import os
import sys
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse

URL = os.environ.get("COLAB_NOTEBOOK_URL", "").strip()

def status():
    print("=== SUPERPLATFORM COLAB CONTROLLER ===")
    print("MODE       : TERMUX CONTROLLER")
    print("BROWSER    : DISABLED")
    print()

    if not URL:
        print("COLAB URL  : NOT CONFIGURED")
        print()
        print("Set it with:")
        print('export COLAB_NOTEBOOK_URL="YOUR_COLAB_NOTEBOOK_URL"')
        return 1

    p = urlparse(URL)

    if p.scheme not in ("http", "https"):
        print("COLAB URL  : INVALID")
        return 1

    print("COLAB URL  : CONFIGURED")
    print("HOST       :", p.netloc)

    try:
        req = urllib.request.Request(
            URL,
            headers={
                "User-Agent": "SuperPlatform-Colab-Controller/1.0"
            }
        )

        with urllib.request.urlopen(req, timeout=20) as r:
            sample = r.read(1000)

            print("HTTP       :", r.status)
            print("ACCESS     : OK")
            print("HTML       :", len(sample), "bytes sampled")

            text = sample.decode("utf-8", errors="ignore").lower()

            if "sign in" in text or "anonymous" in text:
                print("AUTH       : WEB SESSION NOT CONFIRMED")
                print("RUNTIME    : NOT CONFIRMED")
                print()
                print("Colab is reachable, but this HTTP request")
                print("does not prove authenticated runtime access.")
                return 2

            print("AUTH       : NOT DETERMINED")
            print("RUNTIME    : NOT DETERMINED")
            return 0

    except urllib.error.HTTPError as e:
        print("HTTP       :", e.code)
        print("ACCESS     : FAILED")
        return 1

    except Exception as e:
        print("ACCESS     : FAILED")
        print("ERROR      :", repr(e))
        return 1


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "status"

    if command == "status":
        return status()

    if command == "help":
        print("""
SuperPlatform Colab Controller

Commands:
  colabctl status
  colabctl help

Environment:
  COLAB_NOTEBOOK_URL

Note:
  This controller does not store Google passwords,
  browser cookies, or session tokens.
""")
        return 0

    print("UNKNOWN COMMAND:", command)
    print("Use: colabctl help")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
