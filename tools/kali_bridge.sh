#!/data/data/com.termux/files/usr/bin/bash

echo "=========================================="
echo "       SUPER PLATFORM — KALI BRIDGE"
echo "=========================================="
echo

if command -v nh >/dev/null 2>&1; then
    NH="nh"
elif command -v nethunter >/dev/null 2>&1; then
    NH="nethunter"
else
    echo "NetHunter command not found."
    exit 1
fi

echo "[PASS] NetHunter command: $NH"
echo

$NH -r /bin/sh <<'KALI'
echo "===== KALI ENVIRONMENT ====="
echo "Distribution:"
grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null
echo "Architecture: $(uname -m)"
echo

echo "===== CORE TOOLS ====="
for t in nmap python3 git curl wget ssh; do
    if command -v "$t" >/dev/null 2>&1; then
        printf '[AVAILABLE] %s\n' "$t"
    else
        printf '[NOT FOUND] %s\n' "$t"
    fi
done

echo
echo "===== EXECUTABLE INVENTORY ====="
count=0
for d in /usr/bin /usr/sbin; do
    if [ -d "$d" ]; then
        n=$(find "$d" -maxdepth 1 -type f -executable 2>/dev/null | wc -l)
        count=$((count+n))
    fi
done
echo "Executable files: $count"
KALI

result=$?

echo
if [ "$result" -eq 0 ]; then
    echo "===== KALI BRIDGE: PASS ====="
else
    echo "===== KALI BRIDGE: FAIL ====="
fi
