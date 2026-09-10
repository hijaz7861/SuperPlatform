#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/SuperPlatform/agent"
AGENT="$BASE/agent.sh"

while true; do
    clear
    echo "======================================"
    echo "        SUPER PLATFORM AGENT"
    echo "======================================"
    echo
    echo "1) System Status"
    echo "2) Network Status"
    echo "3) Wi-Fi Status"
    echo "4) Storage Status"
    echo "5) Agent Status"
    echo "6) View Agent Log"
    echo "7) Local AI Engine"
    echo "8) Kali / NetHunter"
    echo "0) Exit"
    echo

    read -p "AGENT > " choice

    case "$choice" in
        1) "$AGENT" system; read -p "Press Enter..." ;;
        2) "$AGENT" network; read -p "Press Enter..." ;;
        3) "$AGENT" wifi; read -p "Press Enter..." ;;
        4) "$AGENT" storage; read -p "Press Enter..." ;;
        5) "$AGENT" status; read -p "Press Enter..." ;;
        6)
            echo "===== AGENT LOG ====="
            tail -50 "$HOME/SuperPlatform/logs/agent.log" 2>/dev/null || echo "No log yet."
            read -p "Press Enter..."
            ;;
        7)
            echo "===== LOCAL AI ENGINE ====="
            if [ -x "$HOME/llama.cpp/build/bin/llama-cli" ]; then
                "$HOME/llama.cpp/build/bin/llama-cli" --version
                echo
                echo "Engine: AVAILABLE"
            else
                echo "Engine: NOT FOUND"
            fi
            read -p "Press Enter..."
            ;;
        8)
            echo "===== KALI / NETHUNTER ====="
            if command -v nh >/dev/null 2>&1; then
                nh
            elif command -v nethunter >/dev/null 2>&1; then
                nethunter
            else
                echo "NetHunter not found."
                read -p "Press Enter..."
            fi
            ;;
        0)
            echo "Agent closed."
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
