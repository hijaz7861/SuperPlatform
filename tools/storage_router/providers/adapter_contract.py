#!/usr/bin/env python3
import hashlib
import json
import time
from abc import ABC, abstractmethod
from pathlib import Path


class ProviderAdapter(ABC):
    """
    Universal provider interface.

    External providers are optional.
    Implementations must fail safely without stopping the Core.
    """

    name = "unknown"
    required = False

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def health(self):
        raise NotImplementedError

    @abstractmethod
    def put(self, source, key):
        raise NotImplementedError

    @abstractmethod
    def get(self, key, destination):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key):
        raise NotImplementedError

    @abstractmethod
    def exists(self, key):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError


class OfflineProviderAdapter(ProviderAdapter):
    """
    Safe placeholder adapter for providers that are not connected yet.
    It never pretends that a remote operation succeeded.
    """

    def __init__(self, name):
        self.name = name
        self.required = False
        self.connected = False

    def connect(self):
        self.connected = False
        return {
            "provider": self.name,
            "connected": False,
            "result": "OPTIONAL_OFFLINE"
        }

    def health(self):
        return {
            "provider": self.name,
            "connected": self.connected,
            "available": False,
            "required": False,
            "result": "OFFLINE"
        }

    def put(self, source, key):
        return {
            "provider": self.name,
            "operation": "put",
            "key": key,
            "result": "UNAVAILABLE"
        }

    def get(self, key, destination):
        return {
            "provider": self.name,
            "operation": "get",
            "key": key,
            "result": "UNAVAILABLE"
        }

    def delete(self, key):
        return {
            "provider": self.name,
            "operation": "delete",
            "key": key,
            "result": "UNAVAILABLE"
        }

    def exists(self, key):
        return False

    def disconnect(self):
        self.connected = False
        return {
            "provider": self.name,
            "connected": False,
            "result": "DISCONNECTED"
        }


class LocalProviderAdapter(ProviderAdapter):
    """
    Minimal real local adapter used as the independent fallback.
    """

    name = "local"
    required = False

    def __init__(self, root=None):
        self.root = Path(root or ".").resolve()
        self.data = self.root / "storage" / "data"
        self.data.mkdir(parents=True, exist_ok=True)
        self.connected = False

    def connect(self):
        self.connected = True
        return {
            "provider": self.name,
            "connected": True,
            "result": "PASS"
        }

    def health(self):
        return {
            "provider": self.name,
            "connected": self.connected,
            "available": self.data.is_dir(),
            "required": False,
            "result": "READY" if self.data.is_dir() else "FAIL"
        }

    def _path(self, key):
        digest = hashlib.sha256(str(key).encode()).hexdigest()
        return self.data / digest

    def put(self, source, key):
        source = Path(source)
        target = self._path(key)
        target.write_bytes(source.read_bytes())
        return {
            "provider": self.name,
            "operation": "put",
            "key": key,
            "path": str(target),
            "result": "PASS"
        }

    def get(self, key, destination):
        source = self._path(key)
        if not source.exists():
            return {
                "provider": self.name,
                "operation": "get",
                "key": key,
                "result": "NOT_FOUND"
            }

        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())

        return {
            "provider": self.name,
            "operation": "get",
            "key": key,
            "destination": str(destination),
            "result": "PASS"
        }

    def delete(self, key):
        target = self._path(key)
        if target.exists():
            target.unlink()

        return {
            "provider": self.name,
            "operation": "delete",
            "key": key,
            "result": "PASS"
        }

    def exists(self, key):
        return self._path(key).exists()

    def disconnect(self):
        self.connected = False
        return {
            "provider": self.name,
            "connected": False,
            "result": "DISCONNECTED"
        }


def build_default_adapters(root):
    return {
        "local": LocalProviderAdapter(root),
        "github": OfflineProviderAdapter("github"),
        "google_drive": OfflineProviderAdapter("google_drive"),
        "mega": OfflineProviderAdapter("mega"),
        "cloud": OfflineProviderAdapter("cloud"),
    }


def contract_status(root):
    adapters = build_default_adapters(root)

    for adapter in adapters.values():
        adapter.connect()

    return {
        "system": "RUNNING",
        "adapter_contract": "READY",
        "providers": {
            name: adapter.health()
            for name, adapter in adapters.items()
        },
        "external_optional": all(
            not adapter.required
            for name, adapter in adapters.items()
            if name != "local"
        ),
        "timestamp": time.time()
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    print(json.dumps(contract_status(root), indent=2))
