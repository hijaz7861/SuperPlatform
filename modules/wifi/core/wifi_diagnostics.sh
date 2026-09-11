#!/data/data/com.termux/files/usr/bin/bash

LOG_DIR="$(dirname "$(dirname "$0")")/logs"
mkdir -p "$LOG_DIR"

LOG="$LOG_DIR/wifi_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG") 2>&1

echo "======================================"
echo " SuperPlatform Wi-Fi Diagnostics"
echo " $(date)"
echo "======================================"

echo
echo "[1] Android"
if command -v getprop >/dev/null 2>&1; then
    echo "Model:   $(getprop ro.product.model)"
    echo "Android: $(getprop ro.build.version.release)"
    echo "SDK:     $(getprop ro.build.version.sdk)"
    echo "Board:   $(getprop ro.board.platform)"
    echo "Hardware: $(getprop ro.hardware)"
else
    echo "getprop unavailable"
fi

echo
echo "[2] User / privileges"
id

echo
echo "[3] Interfaces"
if command -v ip >/dev/null 2>&1; then
    ip -br link
else
    echo "ip unavailable"
fi

echo
echo "[4] Wi-Fi interfaces"
if command -v iw >/dev/null 2>&1; then
    iw dev
else
    echo "iw unavailable"
fi

echo
echo "[5] Wireless PHY"
if command -v iw >/dev/null 2>&1; then
    iw phy
else
    echo "iw unavailable"
fi

echo
echo "[6] Sysfs"
if [ -d /sys/class ]; then
    echo "SYSFS CLASS: AVAILABLE"
else
    echo "SYSFS CLASS: UNAVAILABLE"
fi

if [ -d /sys/class/net/wlan0 ]; then
    echo "wlan0 sysfs: AVAILABLE"
else
    echo "wlan0 sysfs: UNAVAILABLE"
fi

echo
echo "[7] Capabilities"
grep '^Cap' /proc/self/status 2>/dev/null || echo "Capability information unavailable"

echo
echo "[8] airmon-ng"
if command -v airmon-ng >/dev/null 2>&1; then
    airmon-ng 2>&1
else
    echo "airmon-ng not installed"
fi

echo
echo "[9] USB"
if command -v termux-usb >/dev/null 2>&1; then
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
    echo "termux-usb unavailable"
fi

echo
echo "======================================"
echo "Diagnostic log:"
echo "$LOG"
echo "======================================"
