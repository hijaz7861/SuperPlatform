#!/data/data/com.termux/files/usr/bin/bash

SCRIPT="$HOME/SuperPlatform/modules/privacy/tor/tor_manager.sh"

echo "===== TOR STRUCTURE TEST ====="

if [ -x "$SCRIPT" ]; then
    echo "SCRIPT: PASS"
else
    echo "SCRIPT: FAIL"
    exit 1
fi

if bash -n "$SCRIPT"; then
    echo "SYNTAX: PASS"
else
    echo "SYNTAX: FAIL"
    exit 1
fi

"$SCRIPT" status
