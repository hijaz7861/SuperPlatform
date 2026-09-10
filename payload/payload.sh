#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$(cd "$(dirname "$0")" && pwd)"

echo "=== SUPERPLATFORM PAYLOAD ==="

python "$BASE/payload.py"

echo
echo "SHELL PAYLOAD: PASS"
