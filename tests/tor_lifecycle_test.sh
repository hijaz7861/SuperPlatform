#!/data/data/com.termux/files/usr/bin/bash

set -u

SUPER="$HOME/SuperPlatform/bin/super"

echo "======================================"
echo " SUPER PLATFORM — TOR LIFECYCLE TEST"
echo "======================================"

echo
echo "[1] STOP"
"$SUPER" privacy tor stop

sleep 2

echo
echo "[2] VERIFY STOP"
if pgrep -x tor >/dev/null 2>&1; then
    echo "STOP TEST: FAIL"
    echo "Tor process is still running."
    exit 1
else
    echo "STOP TEST: PASS"
fi

echo
echo "[3] START"
"$SUPER" privacy tor start

sleep 3

echo
echo "[4] VERIFY RUNNING"
if pgrep -x tor >/dev/null 2>&1; then
    echo "START TEST: PASS"
else
    echo "START TEST: FAIL"
    exit 1
fi

echo
echo "[5] STATUS"
"$SUPER" privacy tor status

echo
echo "[6] PROCESS"
pgrep -a tor || true

echo
echo "======================================"
echo " TOR LIFECYCLE TEST COMPLETE"
echo "======================================"
