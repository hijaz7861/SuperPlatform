#!/data/data/com.termux/files/usr/bin/bash

TOR_LOG="$HOME/SuperPlatform/logs/tor.log"

log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$TOR_LOG"
}

case "${1:-status}" in

status)
    echo "===== TOR STATUS ====="
    if command -v tor >/dev/null 2>&1; then
        echo "Tor binary: AVAILABLE"
        tor --version 2>/dev/null | head -1
    else
        echo "Tor binary: NOT INSTALLED"
        echo "Install with: pkg install tor"
    fi

    if pgrep -x tor >/dev/null 2>&1; then
        echo "Tor process: RUNNING"
    else
        echo "Tor process: STOPPED"
    fi
    ;;

start)
    if ! command -v tor >/dev/null 2>&1; then
        echo "Tor is not installed."
        echo "Run: pkg install tor"
        exit 1
    fi

    if pgrep -x tor >/dev/null 2>&1; then
        echo "Tor is already running."
        exit 0
    fi

    mkdir -p "$HOME/.tor"
    tor > "$HOME/.tor/tor.log" 2>&1 &
    echo $! > "$HOME/.tor/tor.pid"

    sleep 3

    if pgrep -x tor >/dev/null 2>&1; then
        echo "TOR START: PASS"
        log "Tor started"
    else
        echo "TOR START: FAIL"
        log "Tor failed to start"
        exit 1
    fi
    ;;

stop)
    if pgrep -x tor >/dev/null 2>&1; then
        pkill -x tor
        sleep 2
    fi

    if pgrep -x tor >/dev/null 2>&1; then
        echo "TOR STOP: FAIL"
        exit 1
    else
        echo "TOR STOP: PASS"
        log "Tor stopped"
    fi
    ;;

test)
    echo "===== TOR TEST ====="

    if ! command -v tor >/dev/null 2>&1; then
        echo "TOR BINARY: FAIL"
        echo "Install first: pkg install tor"
        exit 1
    fi

    echo "TOR BINARY: PASS"
    tor --version 2>/dev/null | head -1

    if pgrep -x tor >/dev/null 2>&1; then
        echo "TOR PROCESS: PASS"
    else
        echo "TOR PROCESS: NOT RUNNING"
        echo "Start with: super privacy tor start"
    fi

    echo "Configuration directory: $HOME/.tor"
    echo "Log: $TOR_LOG"
    ;;

config)
    echo "===== TOR CONFIG ====="
    echo "Default directory: $HOME/.tor"
    echo "Tor configuration can be managed here:"
    echo "$HOME/.tor"
    ;;

*)
    echo "Usage:"
    echo "  super privacy tor status"
    echo "  super privacy tor start"
    echo "  super privacy tor stop"
    echo "  super privacy tor test"
    echo "  super privacy tor config"
    exit 2
    ;;
esac
