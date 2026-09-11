#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/SuperPlatform/modules/wifi"
STATE="$ROOT/state/wifi_status.json"

timestamp="$(date -Iseconds)"

json_escape() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

sysfs_class="false"
wlan0_sysfs="false"
netlink="false"
wlan0="false"
wlan1="false"
p2p0="false"
airmon="false"
usb="false"

[ -d /sys/class ] && sysfs_class="true"
[ -d /sys/class/net/wlan0 ] && wlan0_sysfs="true"

if command -v ip >/dev/null 2>&1; then
    ip link show wlan0 >/dev/null 2>&1 && wlan0="true"
    ip link show wlan1 >/dev/null 2>&1 && wlan1="true"
    ip link show p2p0 >/dev/null 2>&1 && p2p0="true"
fi

if command -v iw >/dev/null 2>&1; then
    if iw dev >/dev/null 2>&1; then
        netlink="true"
    fi
fi

command -v airmon-ng >/dev/null 2>&1 && airmon="true"

if command -v termux-usb >/dev/null 2>&1; then
    if command -v timeout >/dev/null 2>&1; then
        timeout 3 termux-usb -l >/dev/null 2>&1
        [ "$?" -eq 0 ] && usb="true"
    fi
fi

model="$(getprop ro.product.model 2>/dev/null)"
android="$(getprop ro.build.version.release 2>/dev/null)"
board="$(getprop ro.board.platform 2>/dev/null)"
hardware="$(getprop ro.hardware 2>/dev/null)"

cat > "$STATE" <<JSON
{
  "module": "wifi_engine",
  "timestamp": "$(json_escape "$timestamp")",
  "android": {
    "model": "$(json_escape "$model")",
    "version": "$(json_escape "$android")",
    "board": "$(json_escape "$board")",
    "hardware": "$(json_escape "$hardware")"
  },
  "interfaces": {
    "wlan0": $wlan0,
    "wlan1": $wlan1,
    "p2p0": $p2p0
  },
  "access": {
    "sysfs_class": $sysfs_class,
    "wlan0_sysfs": $wlan0_sysfs,
    "generic_netlink": $netlink,
    "airmon_ng": $airmon,
    "usb_device_visible": $usb
  }
}
JSON

echo "=== WIFI ENGINE RESULT ==="
cat "$STATE"

echo
echo "=== INTERPRETATION ==="

if [ "$wlan0" = true ]; then
    echo "WLAN HARDWARE INTERFACE: DETECTED"
else
    echo "WLAN HARDWARE INTERFACE: NOT DETECTED"
fi

if [ "$netlink" = true ]; then
    echo "WIRELESS NETLINK: AVAILABLE"
else
    echo "WIRELESS NETLINK: BLOCKED/UNAVAILABLE"
fi

if [ "$wlan0_sysfs" = true ]; then
    echo "WLAN SYSFS: AVAILABLE"
else
    echo "WLAN SYSFS: BLOCKED/UNAVAILABLE"
fi

if [ "$airmon" = true ]; then
    echo "AIRMON-NG: INSTALLED"
else
    echo "AIRMON-NG: NOT INSTALLED"
fi

echo
echo "=== MONITOR MODE DIAGNOSTIC ==="

if [ "$wlan0" = true ] &&
   [ "$netlink" = true ] &&
   [ "$wlan0_sysfs" = true ]; then
    echo "KERNEL WIFI CONTROL: POTENTIALLY AVAILABLE"
else
    echo "KERNEL WIFI CONTROL: NOT AVAILABLE FROM CURRENT TERMUX CONTEXT"
fi

echo
echo "State file:"
echo "$STATE"
