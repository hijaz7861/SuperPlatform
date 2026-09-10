#!/data/data/com.termux/files/usr/bin/bash

LOG="$HOME/SuperPlatform/logs/network_privacy.log"

log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"
}

echo "======================================"
echo "     SUPER PLATFORM IP PRIVACY"
echo "======================================"

echo
echo "[1] Network Interfaces"
ip -brief addr 2>/dev/null || echo "ip command unavailable"

echo
echo "[2] Default Gateway"
ip route 2>/dev/null | grep '^default' || echo "No default gateway found"

echo
echo "[3] Local IPv4 Addresses"
ip -4 addr 2>/dev/null | grep -E 'inet ' || echo "No IPv4 address found"

echo
echo "[4] Active Network Connections"
if command -v ss >/dev/null 2>&1; then
    ss -tunp 2>/dev/null || ss -tun 2>/dev/null
else
    echo "ss command unavailable"
fi

echo
echo "[5] DNS Configuration"
if [ -f "$PREFIX/etc/resolv.conf" ]; then
    cat "$PREFIX/etc/resolv.conf"
else
    echo "Termux resolv.conf not found"
fi

echo
echo "[6] Internet Reachability"
if command -v curl >/dev/null 2>&1; then
    if curl -4 -s --max-time 5 https://1.1.1.1/cdn-cgi/trace 2>/dev/null | grep '^ip='; then
        :
    else
        echo "Public IPv4 could not be determined"
    fi
else
    echo "curl unavailable"
fi

echo
echo "[7] Privacy Notes"
echo "- Local IP is normally visible to your LAN/router."
echo "- Public IP is normally visible to internet services you connect to."
echo "- This monitor does not attempt to hide or evade identification."
echo "- Use trusted network/privacy services according to their terms."

log "IP privacy monitor executed"

echo
echo "======================================"
echo "MONITOR COMPLETE"
echo "======================================"
