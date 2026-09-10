#!/data/data/com.termux/files/usr/bin/bash

echo "======================================"
echo "       HIJAZ COIN HEALTH CHECK"
echo "======================================"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo

echo "=== GIT ==="
git branch --show-current
git status --short
git remote -v
echo

echo "=== STORAGE ==="
df -h "$HOME"
echo

echo "=== MEMORY ==="
free -h 2>/dev/null || true
echo

echo "=== CPU ==="
echo "Cores: $(nproc 2>/dev/null || echo unknown)"
uptime
echo

echo "=== PYTHON ==="
python --version 2>&1
echo

echo "=== GIT VERSION ==="
git --version
echo

echo "=== GITHUB CLI ==="
gh --version | head -1
gh auth status 2>&1
echo

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "=== WEBSITE ==="
if [ -f website/index.html ]; then
    echo "website/index.html: PRESENT"
else
    echo "website/index.html: MISSING"
fi

if [ -f docs/index.html ]; then
    echo "docs/index.html: PRESENT"
else
    echo "docs/index.html: MISSING"
fi

echo

echo "=== LOCAL WEBSITE HTTP TEST ==="
WEB_TEST_LOG="$PWD/.hijaz_web_test.log"
python -m http.server 8090 --directory docs >"$WEB_TEST_LOG" 2>&1 &
SERVER_PID=$!

sleep 2

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    http://127.0.0.1:8090/)

kill "$SERVER_PID" 2>/dev/null

if [ "$HTTP_CODE" = "200" ]; then
    echo "HTTP TEST: PASS ($HTTP_CODE)"
else
    echo "HTTP TEST: FAIL ($HTTP_CODE)"
fi

echo

echo "=== GITHUB PAGES ==="
curl -L -s -o /dev/null \
    -w "HTTP: %{http_code}\nURL: %{url_effective}\n" \
    https://hijaz7861.github.io/hijaz-coin/

echo
echo "======================================"
echo "          HEALTH CHECK END"
echo "======================================"
