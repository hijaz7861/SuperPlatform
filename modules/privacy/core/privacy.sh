#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/SuperPlatform"
LOG="$BASE/logs/privacy_core.log"

mkdir -p "$BASE/logs"

log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"
}

show_tor() {
    echo "Tor Binary:"
    if command -v tor >/dev/null 2>&1; then
        echo "  AVAILABLE"
        tor --version 2>/dev/null | head -1
    else
        echo "  NOT INSTALLED"
    fi

    echo "Tor Process:"
    if pgrep -x tor >/dev/null 2>&1; then
        echo "  RUNNING"
    else
        echo "  STOPPED"
    fi
}

show_network() {
    echo "Network:"
    ip -brief addr 2>/dev/null | grep -E 'wlan|rmnet|eth|lo' || \
        echo "  Network information unavailable"
}

show_dns() {
    echo "DNS:"
    if [ -f "$PREFIX/etc/resolv.conf" ]; then
        grep '^nameserver' "$PREFIX/etc/resolv.conf" || \
            echo "  No DNS servers found"
    else
        echo "  DNS configuration unavailable"
    fi
}

show_connections() {
    echo "Connections:"
    if command -v ss >/dev/null 2>&1; then
        ss -tun 2>/dev/null || true
    else
        echo "  ss unavailable"
    fi
}

health() {
    local passed=0

    command -v tor >/dev/null 2>&1 && passed=$((passed+1))
    pgrep -x tor >/dev/null 2>&1 && passed=$((passed+1))
    command -v ip >/dev/null 2>&1 && passed=$((passed+1))
    command -v ss >/dev/null 2>&1 && passed=$((passed+1))

    echo "Health Checks: $passed/4"

    if [ "$passed" -eq 4 ]; then
        echo "HEALTH: GOOD"
    elif [ "$passed" -ge 2 ]; then
        echo "HEALTH: PARTIAL"
    else
        echo "HEALTH: LIMITED"
    fi
}

status() {
    echo "======================================"
    echo " SUPER PLATFORM — PRIVACY CORE"
    echo "======================================"

    echo
    echo "[TOR]"
    show_tor

    echo
    echo "[NETWORK]"
    show_network

    echo
    echo "[DNS]"
    show_dns

    echo
    echo "[CONNECTIONS]"
    show_connections

    echo
    echo "[HEALTH]"
    health

    log "Privacy Core status executed"

    echo
    echo "======================================"
}

case "${1:-status}" in
    status)
        status
        ;;
    tor)
        show_tor
        ;;
    network)
        show_network
        ;;
    dns)
        show_dns
        ;;
    connections)
        show_connections
        ;;
    health)
        health
        ;;
    audit)
        tail -50 "$LOG" 2>/dev/null || echo "No audit log"
        ;;
    *)
        echo "Usage:"
        echo "  privacy.sh status"
        echo "  privacy.sh tor"
        echo "  privacy.sh network"
        echo "  privacy.sh dns"
        echo "  privacy.sh connections"
        echo "  privacy.sh health"
        echo "  privacy.sh audit"
        exit 2
        ;;
esac
