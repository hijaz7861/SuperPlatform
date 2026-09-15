#!/usr/bin/env python3
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STATE = ROOT / "storage" / "provider_state"
STATE.mkdir(parents=True, exist_ok=True)

PROVIDERS = {
    "local": {
        "required": False,
        "enabled": True,
        "available": True,
        "priority": 1
    },
    "github": {
        "required": False,
        "enabled": True,
        "available": False,
        "priority": 2
    },
    "google_drive": {
        "required": False,
        "enabled": True,
        "available": False,
        "priority": 3
    },
    "mega": {
        "required": False,
        "enabled": True,
        "available": False,
        "priority": 4
    },
    "cloud": {
        "required": False,
        "enabled": True,
        "available": False,
        "priority": 5
    }
}


def save_state():
    path = STATE / "providers.json"
    path.write_text(json.dumps(PROVIDERS, indent=2))
    return path


def choose_provider():
    candidates = [
        (name, data)
        for name, data in PROVIDERS.items()
        if data["enabled"] and data["available"]
    ]

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[1]["priority"])
    return candidates[0][0]


def status():
    selected = choose_provider()

    return {
        "system": "RUNNING",
        "provider_contract": "READY",
        "selected_provider": selected,
        "fallback_enabled": True,
        "providers": PROVIDERS,
        "all_external_optional": all(
            not p["required"] for p in PROVIDERS.values()
        ),
        "timestamp": time.time()
    }


def main():
    action = __import__("sys").argv[1] if len(__import__("sys").argv) > 1 else "status"

    if action == "init":
        path = save_state()
        print(json.dumps({
            "provider_state": str(path),
            "result": "PASS"
        }, indent=2))
        return 0

    if action == "select":
        provider = choose_provider()

        if provider is None:
            print(json.dumps({
                "selected_provider": None,
                "fallback": "QUEUE",
                "result": "DEGRADED"
            }, indent=2))
            return 0

        print(json.dumps({
            "selected_provider": provider,
            "fallback": "READY",
            "result": "PASS"
        }, indent=2))
        return 0

    if action == "status":
        print(json.dumps(status(), indent=2))
        return 0

    print("USAGE: provider_contract.py {init|select|status}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
