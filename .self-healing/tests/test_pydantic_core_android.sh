#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "=== PYDANTIC-CORE ANDROID ARM64 REGRESSION ==="

WHEEL="$(find artifacts/android -type f \
  -name 'pydantic_core-*-cp314-cp314-android_24_arm64_v8a.whl' \
  | head -n1)"

[[ -n "$WHEEL" ]] || {
  echo "WHEEL: FAIL"
  exit 1
}

echo "WHEEL: PASS"
echo "FILE=$WHEEL"

PYVER="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "PYTHON=$PYVER"

[[ "$PYVER" == "3.14" ]] || {
  echo "PYTHON_3_14: FAIL"
  exit 2
}

echo "PYTHON_3_14: PASS"

python -m pip install --force-reinstall "$WHEEL"

python - <<'PY'
import pydantic_core
from pydantic_core import SchemaValidator

print("IMPORT: PASS")
print("VERSION:", pydantic_core.__version__)

schema = {
    "type": "typed-dict",
    "fields": {
        "name": {
            "type": "typed-dict-field",
            "schema": {"type": "str"}
        }
    }
}

validator = SchemaValidator(schema)
result = validator.validate_python({"name": "SuperPlatform"})

assert result["name"] == "SuperPlatform"

print("VALIDATION: PASS")
print("RUNTIME: PASS")
PY

python - "$WHEEL" <<'PY'
import sys, zipfile, re

wheel = sys.argv[1]

with zipfile.ZipFile(wheel) as z:
    names = z.namelist()

native = [
    n for n in names
    if re.search(r'\.so$', n)
]

assert any(
    "cpython-314-aarch64-linux-android.so" in n
    for n in native
), "Android ARM64 CPython 3.14 native extension missing"

print("NATIVE_ARM64_EXTENSION: PASS")
PY

cat > .self-healing/state/pydantic-core-android.state <<EOF
STATUS=PASS
VERSION=2.49.0
PYTHON=3.14
ANDROID_API=24
ARCH=arm64_v8a
RUNTIME=PASS
EOF

echo "=== PYDANTIC-CORE ANDROID REGRESSION: PASS ==="
