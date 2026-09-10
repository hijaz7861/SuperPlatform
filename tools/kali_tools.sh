#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/SuperPlatform"

echo "=========================================="
echo "     SUPER PLATFORM — KALI TOOL MANAGER"
echo "=========================================="
echo

if command -v nh >/dev/null 2>&1; then
    NH="nh"
elif command -v nethunter >/dev/null 2>&1; then
    NH="nethunter"
else
    echo "[FAIL] NetHunter not found."
    exit 1
fi

while true; do
    clear

    echo "=========================================="
    echo "     SUPER PLATFORM — KALI TOOL MANAGER"
    echo "=========================================="
    echo
    echo "NetHunter: $NH"
    echo

    TOOLS=()

    while IFS= read -r tool; do
        TOOLS+=("$tool")
    done < <(
        $NH -r /bin/sh -c '
            for d in /usr/bin /usr/sbin; do
                [ -d "$d" ] || continue
                find "$d" -maxdepth 1 -type f -executable 2>/dev/null
            done
        ' 2>/dev/null |
        sed 's#^.*/##' |
        sort -u
    )

    echo "Installed executable tools: ${#TOOLS[@]}"
    echo

    echo " 1) Search Tool"
    echo " 2) Tool Version"
    echo " 3) Tool Help"
    echo " 4) Show Tool Path"
    echo " 5) Refresh Inventory"
    echo " 0) Exit"
    echo

    read -r -p "KALI-TOOLS> " choice

    case "$choice" in

        1)
            read -r -p "Search name: " query

            echo
            echo "===== SEARCH RESULTS ====="

            found=0

            for tool in "${TOOLS[@]}"; do
                case "$tool" in
                    *"$query"*)
                        echo "$tool"
                        found=1
                        ;;
                esac
            done

            [ "$found" -eq 0 ] && echo "No matching tool found."

            echo
            read -r -p "Press Enter..."
            ;;

        2)
            read -r -p "Tool name: " tool

            echo
            echo "===== TOOL VERSION ====="

            if printf '%s\n' "${TOOLS[@]}" | grep -Fxq "$tool"; then
                $NH -r "$tool" --version 2>&1 ||
                $NH -r "$tool" -V 2>&1 ||
                echo "Version information unavailable."
            else
                echo "[BLOCKED] Tool is not in discovered Kali inventory."
            fi

            echo
            read -r -p "Press Enter..."
            ;;

        3)
            read -r -p "Tool name: " tool

            echo
            echo "===== TOOL HELP ====="

            if printf '%s\n' "${TOOLS[@]}" | grep -Fxq "$tool"; then
                $NH -r "$tool" --help 2>&1 ||
                $NH -r "$tool" -h 2>&1 ||
                echo "Help information unavailable."
            else
                echo "[BLOCKED] Tool is not in discovered Kali inventory."
            fi

            echo
            read -r -p "Press Enter..."
            ;;

        4)
            read -r -p "Tool name: " tool

            echo
            echo "===== TOOL PATH ====="

            if printf '%s\n' "${TOOLS[@]}" | grep -Fxq "$tool"; then
                $NH -r command -v "$tool" 2>&1
            else
                echo "[BLOCKED] Tool is not in discovered Kali inventory."
            fi

            echo
            read -r -p "Press Enter..."
            ;;

        5)
            echo "Refreshing Kali tool inventory..."
            sleep 1
            ;;

        0)
            echo "Kali Tool Manager closed."
            exit 0
            ;;

        *)
            echo "Invalid option."
            sleep 1
            ;;
    esac
done
