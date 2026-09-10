#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/SuperPlatform"
AGENT="$BASE/agent/agent.sh"
CONTROL="$BASE/agent/control.sh"
LOG="$BASE/logs/agent.log"

while true; do
    clear
    echo "================================================"
    echo "        SUPER PLATFORM — TERMUX CORE"
    echo "================================================"
    echo
    echo " 1) Agent Status"
    echo " 2) System"
    echo " 3) Network"
    echo " 4) Wi-Fi"
    echo " 5) Storage"
    echo " 6) Security"
    echo " 7) Interactive Agent"
    echo " 8) Local AI / llama.cpp"
    echo " 9) Kali / NetHunter"
    echo "10) Agent Logs"
    echo "11) Show All Project Files"
    echo "12) Check All Scripts"
    echo "13) Kali Tool Manager"
    echo " 0) Exit"
    echo
    read -r -p "SUPER> " choice

    case "$choice" in
        1)
            "$AGENT" status
            read -r -p "Enter..."
            ;;
        2)
            "$AGENT" system
            read -r -p "Enter..."
            ;;
        3)
            "$AGENT" network
            read -r -p "Enter..."
            ;;
        4)
            "$AGENT" wifi
            read -r -p "Enter..."
            ;;
        5)
            "$AGENT" storage
            read -r -p "Enter..."
            ;;
        6)
            echo "===== SECURITY ====="
            echo "Policy:"
            cat "$BASE/agent/policy.sh"
            echo
            echo "Executable scripts:"
            find "$BASE" -type f -name "*.sh" -perm -u+x -print
            read -r -p "Enter..."
            ;;
        7)
            "$CONTROL"
            ;;
        8)
            echo "===== LOCAL AI / LLAMA.CPP ====="
            if [ -x "$HOME/llama.cpp/build/bin/llama-cli" ]; then
                "$HOME/llama.cpp/build/bin/llama-cli" --version
                echo
                echo "Engine: AVAILABLE"
            else
                echo "Engine: NOT FOUND"
            fi
            read -r -p "Enter..."
            ;;
        9)
            echo "===== KALI / NETHUNTER ====="
            if command -v nh >/dev/null 2>&1; then
                nh
            elif command -v nethunter >/dev/null 2>&1; then
                nethunter
            else
                echo "NetHunter: NOT FOUND"
                read -r -p "Enter..."
            fi
            ;;
        10)
            echo "===== AGENT LOG ====="
            tail -100 "$LOG" 2>/dev/null || echo "No log found."
            read -r -p "Enter..."
            ;;
        11)
            echo "===== SUPERPLATFORM FILES ====="
            find "$BASE" -type f -print | sort | nl -w2 -s') '
            read -r -p "Enter..."
            ;;
        12)
            echo "===== SCRIPT CHECK ====="
            failed=0
            while IFS= read -r file; do
                if bash -n "$file"; then
                    echo "PASS: $file"
                else
                    echo "FAIL: $file"
                    failed=1
                fi
            done < <(find "$BASE" -type f -name "*.sh" | sort)

            echo
            if [ "$failed" -eq 0 ]; then
                echo "ALL SCRIPT SYNTAX CHECKS PASSED"
            else
                echo "ONE OR MORE SCRIPTS FAILED"
            fi
            read -r -p "Enter..."
            ;;
        13)
            "$BASE/tools/kali_tools.sh"
            ;;

        0)
            echo "SUPER PLATFORM CLOSED"
            exit 0
            ;;
        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
