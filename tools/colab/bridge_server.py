#!/usr/bin/env python3

import os
import json
import subprocess
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = int(os.environ.get("COLAB_BRIDGE_PORT", "8765"))
TOKEN_FILE = os.path.expanduser("~/.superplatform_colab_bridge_token")

if os.path.exists(TOKEN_FILE):
    TOKEN = open(TOKEN_FILE).read().strip()
else:
    TOKEN = secrets.token_urlsafe(32)
    with open(TOKEN_FILE, "w") as f:
        f.write(TOKEN)
    os.chmod(TOKEN_FILE, 0o600)

class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        return self.headers.get("X-SuperPlatform-Token", "") == TOKEN

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {
                "ok": True,
                "service": "SuperPlatform Colab Runtime Bridge"
            })
            return

        self.send_json(404, {"ok": False, "error": "not_found"})

    def do_POST(self):
        if not self.authorized():
            self.send_json(401, {
                "ok": False,
                "error": "unauthorized"
            })
            return

        if self.path != "/execute":
            self.send_json(404, {
                "ok": False,
                "error": "not_found"
            })
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))

            code = payload.get("code", "")

            if not isinstance(code, str) or not code.strip():
                self.send_json(400, {
                    "ok": False,
                    "error": "code_required"
                })
                return

            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=120
            )

            self.send_json(200, {
                "ok": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })

        except subprocess.TimeoutExpired:
            self.send_json(408, {
                "ok": False,
                "error": "execution_timeout"
            })

        except Exception as e:
            self.send_json(500, {
                "ok": False,
                "error": repr(e)
            })

    def log_message(self, *args):
        return

print("=== SUPERPLATFORM COLAB RUNTIME BRIDGE ===")
print("HOST  :", HOST)
print("PORT  :", PORT)
print("TOKEN :", TOKEN_FILE)
print("STATUS: READY")
print()
print("Waiting for commands...")

HTTPServer((HOST, PORT), Handler).serve_forever()
