#!/data/data/com.termux/files/usr/bin/bash

execute_task() {
    case "$1" in

        system)
            echo "===== SYSTEM ====="
            uname -a
            echo
            echo "CPU:"
            nproc 2>/dev/null
            echo
            echo "Memory:"
            free -h 2>/dev/null
            ;;

        network)
            echo "===== NETWORK ====="
            ip -br addr 2>/dev/null
            echo
            echo "Routes:"
            ip route 2>/dev/null
            ;;

        wifi)
            echo "===== WIFI STATUS ====="
            echo
            echo "--- Interface ---"
            ip addr show wlan0 2>/dev/null || echo "wlan0 not found"
            echo
            echo "--- Route ---"
            ip route 2>/dev/null
            echo
            echo "--- Connection Info ---"
            if command -v termux-wifi-connectioninfo >/dev/null 2>&1; then
                timeout 8 termux-wifi-connectioninfo 2>&1 || true
            else
                echo "Termux:API unavailable"
            fi
            echo
            echo "--- Wi-Fi Scan ---"
            if command -v termux-wifi-scaninfo >/dev/null 2>&1; then
                timeout 10 termux-wifi-scaninfo 2>&1 || true
            else
                echo "Wi-Fi scan API unavailable"
            fi
            ;;

        storage)
            echo "===== STORAGE ====="
            df -h
            ;;

        status)
            echo "===== AGENT STATUS ====="
            echo "Agent: ONLINE"
            echo "Termux: AVAILABLE"
            echo "Time: $(date)"
            ;;

        *)
            echo "Unknown task"
            return 1
            ;;
    esac
}
