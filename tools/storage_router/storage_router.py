#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORAGE = ROOT / "storage"
LOCAL = STORAGE / "local" / "data"
QUEUE = STORAGE / "queue"
MANIFESTS = STORAGE / "manifests"

for p in (LOCAL, QUEUE, MANIFESTS):
    p.mkdir(parents=True, exist_ok=True)



# STEP21_PROVIDER_INTEGRATION
# Provider selection is optional. Local operation remains available
# when every external provider is offline.
import importlib.util as _sp_importlib_util

_SP_ROOT = Path(__file__).resolve().parents[2]
_SP_PROVIDER_FILE = (
    _SP_ROOT / "tools" / "storage_router" /
    "providers" / "provider_contract.py"
)

def _sp_provider_status():
    spec = _sp_importlib_util.spec_from_file_location(
        "sp_provider_contract",
        _SP_PROVIDER_FILE
    )
    if spec is None or spec.loader is None:
        return {
            "provider_contract": "UNAVAILABLE",
            "selected_provider": "local",
            "fallback": True
        }

    module = _sp_importlib_util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.status()

def selected_provider():
    status = _sp_provider_status()
    provider = status.get("selected_provider")

    if provider:
        return provider

    return "local"

def provider_health():
    status = _sp_provider_status()
    return {
        "system": status.get("system"),
        "provider_contract": status.get("provider_contract"),
        "selected_provider": status.get("selected_provider") or "local",
        "fallback_enabled": status.get("fallback_enabled", True),
        "all_external_optional": status.get(
            "all_external_optional", True
        )
    }

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def put(source, key):
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(source)

    target = LOCAL / key
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

    manifest = {
        "key": key,
        "provider": "local",
        "path": str(target),
        "size": target.stat().st_size,
        "sha256": sha256(target),
        "timestamp": time.time(),
        "external_sync": "optional"
    }

    (MANIFESTS / (key.replace("/", "__") + ".json")).write_text(
        json.dumps(manifest, indent=2)
    )

    return manifest


def get(key, destination):
    source = LOCAL / key
    if not source.is_file():
        raise FileNotFoundError(source)

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

    return {
        "key": key,
        "provider": "local",
        "destination": str(destination),
        "sha256": sha256(destination)
    }


def exists(key):
    return (LOCAL / key).is_file()


def queue_sync(key, provider):
    item = {
        "action": "sync",
        "key": key,
        "target_provider": provider,
        "created": time.time(),
        "status": "PENDING"
    }

    filename = (
        hashlib.sha256(
            f"{key}:{provider}:{time.time_ns()}".encode()
        ).hexdigest() + ".json"
    )

    path = QUEUE / filename
    path.write_text(json.dumps(item, indent=2))

    return item


def status():
    providers = {
        "local": {
            "available": True,
            "required": True
        },
        "github": {
            "available": False,
            "required": False
        },
        "google_drive": {
            "available": False,
            "required": False
        },
        "mega": {
            "available": False,
            "required": False
        },
        "cloud": {
            "available": False,
            "required": False
        }
    }

    return {
        "system": "RUNNING",
        "storage_router": "READY",
        "required_provider": "local",
        "providers": providers,
        "pending_sync_jobs": len(list(QUEUE.glob("*.json"))),
        "offline_external_mode": True
    }


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"

    if action == "put":
        print(json.dumps(put(sys.argv[2], sys.argv[3]), indent=2))

    elif action == "get":
        print(json.dumps(get(sys.argv[2], sys.argv[3]), indent=2))

    elif action == "exists":
        print(json.dumps({
            "key": sys.argv[2],
            "exists": exists(sys.argv[2])
        }, indent=2))

    elif action == "queue":
        print(json.dumps(
            queue_sync(sys.argv[2], sys.argv[3]),
            indent=2
        ))

    elif action == "status":
        print(json.dumps(status(), indent=2))

    else:
        print("USAGE: storage_router.py {status|put|get|exists|queue}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
