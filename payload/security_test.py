import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.security.core import SecurityPolicy

policy = SecurityPolicy()

assert policy.allowed("read_config") is True
assert policy.allowed("delete_system") is False
assert policy.allowed("format_disk") is False
assert policy.allowed("credential_theft") is False
assert policy.allowed("unauthorized_access") is False
assert policy.allowed("external_execution") is False

print("SAFE ACTION TEST: PASS")
print("BLOCKED ACTION TEST: PASS")
print("EXTERNAL EXECUTION DEFAULT: PASS")
print("SECURITY POLICY: PASS")
