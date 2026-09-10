#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$HOME/SuperPlatform"
PASS=0
FAIL=0

check_dir() {
    if [ -d "$ROOT/$1" ]; then
        echo "DIR  PASS: $1"
        PASS=$((PASS+1))
    else
        echo "DIR  FAIL: $1"
        FAIL=$((FAIL+1))
    fi
}

check_dir agent
check_dir modules
check_dir modules/system
check_dir modules/network
check_dir modules/wifi
check_dir modules/storage
check_dir modules/security
check_dir modules/privacy
check_dir tools
check_dir backups
check_dir config
check_dir tests
check_dir bin
check_dir payload

echo
echo "=== PAYLOAD SELF TEST ==="
if python "$ROOT/payload/payload.py"; then
    echo "PYTHON PAYLOAD: PASS"
    PASS=$((PASS+1))
else
    echo "PYTHON PAYLOAD: FAIL"
    FAIL=$((FAIL+1))
fi

echo
echo "=== SHELL SYNTAX ==="
if bash -n "$ROOT/payload/payload.sh"; then
    echo "PAYLOAD SHELL: PASS"
    PASS=$((PASS+1))
else
    echo "PAYLOAD SHELL: FAIL"
    FAIL=$((FAIL+1))
fi

echo
echo "=== INTEGRATION SUMMARY ==="
echo "PASS=$PASS"
echo "FAIL=$FAIL"

if [ "$FAIL" -eq 0 ]; then
    echo "CORE INTEGRATION: PASS"
    exit 0
else
    echo "CORE INTEGRATION: FAIL"
    exit 1
fi
