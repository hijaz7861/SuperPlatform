#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/SuperPlatform"
CORE="$BASE/modules/privacy/core/privacy.sh"

echo "======================================"
echo " SUPER PRIVACY CORE TEST"
echo "======================================"

if [ -x "$CORE" ]; then
    echo "CORE FILE: PASS"
else
    echo "CORE FILE: FAIL"
    exit 1
fi

if bash -n "$CORE"; then
    echo "SYNTAX: PASS"
else
    echo "SYNTAX: FAIL"
    exit 1
fi

echo
echo "[1] HEALTH"
"$CORE" health

echo
echo "[2] TOR"
"$CORE" tor

echo
echo "[3] NETWORK"
"$CORE" network

echo
echo "[4] DNS"
"$CORE" dns

echo
echo "[5] CONNECTIONS"
"$CORE" connections

echo
echo "======================================"
echo " PRIVACY CORE TEST COMPLETE"
echo "======================================"
