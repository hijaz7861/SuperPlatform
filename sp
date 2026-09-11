#!/usr/bin/env python3
import sys
import os
import json
import subprocess
import urllib.request

SERVER = os.environ.get("SUPERPLATFORM_SERVER", "").strip()

def remote(command):
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

    with urllib.request.urlopen(req, timeout=30) as response:
        print(response.read().decode())

def local(command):
    print("MODE: LOCAL")
    print("COMMAND:", command)
    print("STATUS: LOCAL WORKER NOT YET ENABLED")
    print("Remote server is not configured.")
    print("Use 'sp status' for capability detection.")

def main():
    if len(sys.argv) < 2:
        print('Usage: sp "your command"')
        sys.exit(1)

    command = " ".join(sys.argv[1:])

    if SERVER:
        try:
            print("MODE: REMOTE")
            remote(command)
            return
        except Exception as e:
            print("REMOTE UNAVAILABLE:", e)
            print("FALLBACK: LOCAL")

    local(command)

if __name__ == "__main__":
    main()
