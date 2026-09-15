#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "tools" / "storage_router" / "providers" / "adapter_contract.py"
QUEUE = ROOT / "storage" / "queue"
STATE = ROOT / "storage" / "provider_state"

QUEUE.mkdir(parents=True, exist_ok=True)
STATE.mkdir(parents=True, exist_ok=True)


def load_contract():
    spec = importlib.util.spec_from_file_location(
        "sp_adapter_contract",
        CONTRACT
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("ADAPTER_CONTRACT_UNAVAILABLE")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def available_adapters():
    module = load_contract()
    adapters = module.build_default_adapters(ROOT)

    for adapter in adapters.values():
        adapter.connect()

    return adapters


def provider_order(adapters):
    priority = {
        "local": 1,
        "github": 2,
        "google_drive": 3,
        "mega": 4,
        "cloud": 5,
    }

    return sorted(
        adapters,
        key=lambda name: priority.get(name, 999)
    )


def queue_job(operation, source, key, reason, attempted):
    digest = hashlib.sha256(
        f"{operation}:{source}:{key}:{time.time_ns()}".encode()
    ).hexdigest()

    job = {
        "schema_version": "1.0",
        "job_id": digest,
        "operation": operation,
        "source": str(source),
        "key": str(key),
        "reason": reason,
        "attempted_providers": attempted,
        "status": "PENDING",
        "created_at": time.time(),
        "updated_at": time.time(),
        "retry_count": 0,
    }

    path = QUEUE / f"{digest}.json"
    path.write_text(json.dumps(job, indent=2))

    return path


def put_with_failover(source, key):
    adapters = available_adapters()
    attempted = []

    for name in provider_order(adapters):
        adapter = adapters[name]
        health = adapter.health()

        if not health.get("available", False):
            attempted.append({
                "provider": name,
                "result": "UNAVAILABLE"
            })
            continue

        attempted.append({
            "provider": name,
            "result": "ATTEMPT"
        })

        try:
            result = adapter.put(source, key)

            if result.get("result") == "PASS":
                return {
                    "system": "RUNNING",
                    "operation": "put",
                    "provider": name,
                    "fallback_used": name != "local",
                    "result": "PASS",
                    "attempted": attempted,
                }

            attempted[-1]["result"] = result.get(
                "result", "FAILED"
            )

        except Exception as exc:
            attempted[-1]["result"] = "ERROR"
            attempted[-1]["error"] = type(exc).__name__

    queue_path = queue_job(
        "put",
        source,
        key,
        "NO_PROVIDER_AVAILABLE",
        attempted,
    )

    return {
        "system": "RUNNING",
        "operation": "put",
        "provider": None,
        "fallback_used": True,
        "queue": str(queue_path),
        "result": "QUEUED",
        "attempted": attempted,
    }


def status():
    adapters = available_adapters()

    return {
        "system": "RUNNING",
        "failover_engine": "READY",
        "providers": {
            name: adapter.health()
            for name, adapter in adapters.items()
        },
        "queue_directory": str(QUEUE),
        "timestamp": time.time(),
    }


def main():
    import sys

    action = sys.argv[1] if len(sys.argv) > 1 else "status"

    if action == "status":
        print(json.dumps(status(), indent=2))
        return 0

    if action == "test":
        test_file = QUEUE / ".step23-source"
        test_file.write_bytes(b"SUPERPLATFORM-STEP23")

        result = put_with_failover(
            test_file,
            "step23-failover-test"
        )

        if result["result"] != "PASS":
            raise SystemExit(
                "LOCAL_FAILOVER_TEST_FAILED"
            )

        print(json.dumps(result, indent=2))

        local = load_contract().LocalProviderAdapter(ROOT)

        assert local.exists("step23-failover-test")
        assert local.delete(
            "step23-failover-test"
        )["result"] == "PASS"

        test_file.unlink(missing_ok=True)

        print("FAILOVER_OPERATION=PASS")
        print("LOCAL_FALLBACK=PASS")
        print("TEST_CLEANUP=PASS")
        return 0

    if action == "offline-test":
        adapters = available_adapters()

        for name in (
            "github",
            "google_drive",
            "mega",
            "cloud",
        ):
            health = adapters[name].health()
            assert health["available"] is False
            assert health["required"] is False

        print("EXTERNAL_OFFLINE=PASS")
        print("EXTERNAL_OPTIONAL=PASS")
        print("FAILOVER_SAFE=PASS")
        return 0

    print(
        "USAGE: failover_engine.py "
        "{status|test|offline-test}"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
