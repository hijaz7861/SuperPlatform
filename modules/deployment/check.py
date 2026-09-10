from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

required = [
    "agent",
    "modules",
    "modules/system",
    "modules/network",
    "modules/wifi",
    "modules/storage",
    "modules/security",
    "modules/privacy",
    "modules/ledger",
    "modules/deployment",
    "tools",
    "backups",
    "config",
    "tests",
    "logs",
    "bin",
    "payload",
]

failed = 0

for item in required:
    path = ROOT / item

    if path.is_dir():
        print(f"PASS: {item}")
    else:
        print(f"FAIL: {item}")
        failed += 1

if failed == 0:
    print("DEPLOYMENT STRUCTURE: PASS")
else:
    print(f"DEPLOYMENT STRUCTURE: FAIL ({failed})")
    raise SystemExit(1)
