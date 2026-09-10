#!/data/data/com.termux/files/usr/bin/bash

LOG_DIR="$HOME/SuperPlatform/logs"
mkdir -p "$LOG_DIR"

log_event() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" \
        >> "$LOG_DIR/agent.log"
}
