#!/data/data/com.termux/files/usr/bin/bash

set -u

ROOT="$HOME/SuperPlatform/modules/wifi"
CORE="$ROOT/core"
BIN="$ROOT/bin"
STATE="$ROOT/state"
LOG="$ROOT/logs"

mkdir -p "$STATE" "$LOG"

RUN_ID="$(date +%Y%m%d_%H%M%S)"
REPORT="$STATE/report_$RUN_ID.json"
TEXTLOG="$LOG/run_$RUN_ID.log"

exec > >(tee -a "$TEXTLOG") 2>&1

have() {
    command -v "$1" >/dev/null 2>&1
}

status() {
    printf '%-32s : %s\n' "$1" "$2"
}

echo "=========================================="
echo " SuperPlatform Intelligent Wi-Fi Agent v2"
echo " Run: $RUN_ID"
echo "=========================================="

# ------------------------------------------------
# DEVICE DETECTION
# ------------------------------------------------

MODEL="$(getprop ro.product.model 2>/dev/null || true)"
ANDROID="$(getprop ro.build.version.release 2>/dev/null || true)"
SDK="$(getprop ro.build.version.sdk 2>/dev/null || true)"
BOARD="$(getprop ro.board.platform 2>/dev/null || true)"
HARDWARE="$(getprop ro.hardware 2>/dev/null || true)"

WLAN0=false
WLAN1=false
P2P0=false

if have ip; then
    ip link show wlan0 >/dev/null 2>&1 && WLAN0=true
    ip link show wlan1 >/dev/null 2>&1 && WLAN1=true
    ip link show p2p0 >/dev/null 2>&1 && P2P0=true
fi

SYSFS=false
WLAN0_SYSFS=false

[ -d /sys/class ] && SYSFS=true
[ -d /sys/class/net/wlan0 ] && WLAN0_SYSFS=true

NETLINK=false

if have iw; then
    iw dev >/dev/null 2>&1 && NETLINK=true
fi

AIRMON=false
have airmon-ng && AIRMON=true

USB=false

if have termux-usb; then
    if command -v timeout >/dev/null 2>&1; then
        timeout 3 termux-usb -l >/dev/null 2>&1 && USB=true
    else
        USB=false
    fi
fi

CAP_EFFECTIVE="unknown"

if [ -r /proc/self/status ]; then
    CAP_EFFECTIVE="$(grep '^CapEff:' /proc/self/status 2>/dev/null | awk '{print $2}')"
fi

# ------------------------------------------------
# REPORT
# ------------------------------------------------

echo
echo "=== DEVICE ==="

status "Model" "$MODEL"
status "Android" "$ANDROID"
status "SDK" "$SDK"
status "Board" "$BOARD"
status "Hardware" "$HARDWARE"

echo
echo "=== INTERFACES ==="

status "wlan0" "$WLAN0"
status "wlan1" "$WLAN1"
status "p2p0" "$P2P0"

echo
echo "=== ACCESS ==="

status "/sys/class" "$SYSFS"
status "wlan0 sysfs" "$WLAN0_SYSFS"
status "generic netlink" "$NETLINK"
status "capabilities" "$CAP_EFFECTIVE"

echo
echo "=== TOOLS ==="

status "iw" "$(have iw && echo installed || echo missing)"
status "airmon-ng" "$AIRMON"
status "termux-usb" "$(have termux-usb && echo installed || echo missing)"

# ------------------------------------------------
# ERROR ENGINE
# ------------------------------------------------

ERROR_COUNT=0
FIX_COUNT=0

echo
echo "=== ERROR ENGINE ==="

if ! [ "$WLAN0" = true ]; then
    echo "ERROR: wlan0 not detected"
    ERROR_COUNT=$((ERROR_COUNT + 1))
else
    echo "OK: wlan0 detected"
fi

if ! [ "$NETLINK" = true ]; then
    echo "ERROR: generic netlink unavailable"
    ERROR_COUNT=$((ERROR_COUNT + 1))
else
    echo "OK: generic netlink available"
fi

if ! [ "$WLAN0_SYSFS" = true ]; then
    echo "ERROR: wlan0 sysfs unavailable"
    ERROR_COUNT=$((ERROR_COUNT + 1))
else
    echo "OK: wlan0 sysfs available"
fi

if [ "$CAP_EFFECTIVE" = "0000000000000000" ]; then
    echo "INFO: effective Linux capabilities are zero"
fi

# ------------------------------------------------
# SAFE SELF REPAIR
# ------------------------------------------------

echo
echo "=== SAFE SELF-REPAIR ==="

for FILE in \
    "$CORE/wifi_ai.sh" \
    "$BIN/wifi_agent" \
    "$BIN/wifi_status"
do
    if [ -f "$FILE" ] && [ ! -x "$FILE" ]; then
        chmod +x "$FILE" 2>/dev/null && {
            echo "FIXED: executable permission -> $FILE"
            FIX_COUNT=$((FIX_COUNT + 1))
        }
    fi
done

echo "Repair attempts: $FIX_COUNT"

# ------------------------------------------------
# CAPABILITY ANALYSIS
# ------------------------------------------------

CAPABILITY="diagnostic-only"
REASON=""

if [ "$WLAN0" = true ] &&
   [ "$NETLINK" = true ] &&
   [ "$WLAN0_SYSFS" = true ]; then

    CAPABILITY="kernel-wifi-control-potentially-available"
    REASON="Required interface, sysfs and netlink checks are accessible."

else

    CAPABILITY="diagnostic-only"
    REASON="Termux lacks one or more kernel Wi-Fi control interfaces."
fi

echo
echo "=== CAPABILITY ==="
echo "$CAPABILITY"
echo "$REASON"

# ------------------------------------------------
# COMMAND ENGINE
# ------------------------------------------------

run_command() {

    CMD="${1:-status}"

    echo
    echo "=== COMMAND ENGINE ==="
    echo "Requested: $CMD"

    case "$CMD" in

        status|check|diagnose)

            echo "Complete diagnostic already executed."
            ;;

        interfaces)

            echo "--- Network interfaces ---"

            if have ip; then
                ip -br link
            else
                echo "ERROR: ip unavailable"
            fi
            ;;

        wifi)

            echo "--- Wi-Fi interfaces ---"

            if have ip; then
                ip -br link | grep -E 'wlan|p2p' || true
            fi

            echo
            echo "--- iw dev ---"

            if have iw; then
                iw dev 2>&1 || true
            else
                echo "ERROR: iw unavailable"
            fi
            ;;

        phy)

            echo "--- Wireless PHY ---"

            if have iw; then
                iw phy 2>&1 || true
            else
                echo "ERROR: iw unavailable"
            fi
            ;;

        usb)

            echo "--- USB devices ---"

            if have termux-usb; then
                if command -v timeout >/dev/null 2>&1; then
                    timeout 3 termux-usb -l 2>&1
                    RC=$?
                    if [ "$RC" -eq 124 ]; then
                        echo "WARN: termux-usb timed out after 3 seconds."
                    fi
                else
                    echo "WARN: timeout unavailable; USB enumeration skipped safely."
                fi
            else
                echo "ERROR: termux-usb unavailable"
            fi
            ;;

        repair)

            echo "--- Safe repair ---"

            chmod +x "$CORE"/*.sh 2>/dev/null || true
            chmod +x "$BIN"/* 2>/dev/null || true

            echo "Repair completed."
            ;;

        airmon)

            echo "--- Airmon diagnostic ---"

            if have airmon-ng; then
                airmon-ng 2>&1 || true
            else
                echo "airmon-ng is not installed."
                echo "No Android security bypass will be attempted."
            fi
            ;;

        report)

            echo "--- Latest reports ---"
            ls -1t "$STATE"/report_*.json 2>/dev/null | head -10
            ;;

        logs)

            echo "--- Latest logs ---"
            ls -1t "$LOG"/run_*.log 2>/dev/null | head -10
            ;;

        *)

            echo "Unknown command: $CMD"
            echo
            echo "Available commands:"
            echo "  status"
            echo "  check"
            echo "  diagnose"
            echo "  interfaces"
            echo "  wifi"
            echo "  phy"
            echo "  usb"
            echo "  repair"
            echo "  airmon"
            echo "  report"
            echo "  logs"
            ;;
    esac
}

# ------------------------------------------------
# JSON STATE
# ------------------------------------------------

cat > "$REPORT" <<JSON
{
  "module": "superplatform_wifi_ai",
  "version": "2.0",
  "run_id": "$RUN_ID",
  "device": {
    "model": "$MODEL",
    "android": "$ANDROID",
    "sdk": "$SDK",
    "board": "$BOARD",
    "hardware": "$HARDWARE"
  },
  "interfaces": {
    "wlan0": $WLAN0,
    "wlan1": $WLAN1,
    "p2p0": $P2P0
  },
  "access": {
    "sysfs": $SYSFS,
    "wlan0_sysfs": $WLAN0_SYSFS,
    "generic_netlink": $NETLINK,
    "effective_capabilities": "$CAP_EFFECTIVE"
  },
  "tools": {
    "iw": $(have iw && echo true || echo false),
    "airmon_ng": $AIRMON,
    "termux_usb": $(have termux-usb && echo true || echo false)
  },
  "engine": {
    "errors": $ERROR_COUNT,
    "safe_repairs": $FIX_COUNT,
    "capability": "$CAPABILITY",
    "reason": "$REASON"
  }
}
JSON

echo
echo "=== JSON STATE CREATED ==="
cat "$REPORT"

# ------------------------------------------------
# USER COMMAND
# ------------------------------------------------

run_command "${1:-status}"

echo
echo "=========================================="
echo " AGENT FINISHED"
echo "=========================================="
echo "Report: $REPORT"
echo "Log:    $TEXTLOG"
