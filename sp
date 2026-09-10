#!/usr/bin/env python3

import sys
import os
import json
import urllib.request
import urllib.error

SERVER = os.environ.get("SUPERPLATFORM_SERVER", "")

def send_command(command):
    if not SERVER:
        print("SUPERPLATFORM_SERVER is not configured.")
        print("Remote server address is required.")
        sys.exit(1)

    payload = json.dumps({
        "command": command,
        "project": "SuperPlatform",
        "auto_fix": True
    }).encode()

    req = urllib.request.Request(
        SERVER.rstrip("/") + "/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            print(response.read().decode())
    except Exception as e:
        print("REMOTE CONNECTION ERROR:")
        print(e)
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: sp "your command"')
        sys.exit(1)

    send_command(" ".join(sys.argv[1:]))
