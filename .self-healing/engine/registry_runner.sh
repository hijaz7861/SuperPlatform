#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REGISTRY="$ROOT/.self-healing/registry"
REPORT_DIR="$ROOT/.self-healing/reports"
STATE_DIR="$ROOT/.self-healing/state"

mkdir -p "$REPORT_DIR" "$STATE_DIR"

REPORT="$REPORT_DIR/registry-run-$(date +%Y%m%d_%H%M%S).log"
TOTAL=0
PASS=0
FAIL=0
BLOCKED=0

exec > >(tee "$REPORT") 2>&1

echo "=== SUPERPLATFORM CENTRAL REGISTRY RUNNER ==="
echo "START=$(date -Is)"

shopt -s nullglob
registries=("$REGISTRY"/*.json)

if (( ${#registries[@]} == 0 )); then
    echo "REGISTRY: EMPTY"
    exit 2
fi

for registry in "${registries[@]}"; do
    TOTAL=$((TOTAL+1))

    echo
    echo "========================================"
    echo "REGISTRY: $registry"
    echo "========================================"

    test_path="$(python - "$registry" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print(d["test"])
PY
)"

    module_id="$(python - "$registry" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print(d["id"])
PY
)"

    echo "MODULE=$module_id"
    echo "TEST=$test_path"

    if [[ ! -x "$ROOT/$test_path" ]]; then
        echo "RESULT=BLOCKED"
        BLOCKED=$((BLOCKED+1))
        printf 'STATUS=BLOCKED\nMODULE=%s\nREASON=test_not_executable\n' \
          "$module_id" > "$STATE_DIR/$module_id.runner.state"
        continue
    fi

    set +e
    "$ROOT/$test_path"
    rc=$?
    set -e

    if (( rc == 0 )); then
        echo "RESULT=PASS"
        PASS=$((PASS+1))
        printf 'STATUS=PASS\nMODULE=%s\nEXIT_CODE=0\n' \
          "$module_id" > "$STATE_DIR/$module_id.runner.state"
    else
        echo "RESULT=FAIL"
        echo "EXIT_CODE=$rc"
        FAIL=$((FAIL+1))
        printf 'STATUS=FAIL\nMODULE=%s\nEXIT_CODE=%s\n' \
          "$module_id" "$rc" > "$STATE_DIR/$module_id.runner.state"
    fi
done

echo
echo "========================================"
echo "=== CENTRAL REGISTRY SUMMARY ==="
echo "TOTAL=$TOTAL"
echo "PASS=$PASS"
echo "FAIL=$FAIL"
echo "BLOCKED=$BLOCKED"
echo "REPORT=$REPORT"
echo "========================================"

cat > "$STATE_DIR/registry-runner.state" <<EOF
TOTAL=$TOTAL
PASS=$PASS
FAIL=$FAIL
BLOCKED=$BLOCKED
REPORT=$REPORT
COMPLETED_AT=$(date -Is)
EOF

if (( FAIL > 0 || BLOCKED > 0 )); then
    echo "REGISTRY_RUNNER=NOT_PASS"
    exit 1
fi

echo "REGISTRY_RUNNER=PASS"
