
"""
SuperPlatform Universal Core Registry
"""

from typing import Any, Dict


class UniversalRegistry:

    def __init__(self):
        self.modules: Dict[str, Any] = {}
        self.engines: Dict[str, Any] = {}
        self.providers: Dict[str, Any] = {}

    def register_module(self, name: str, module: Any):
        if not name:
            raise ValueError("Module name required")
        self.modules[name] = module

    def register_engine(self, name: str, engine: Any):
        if not name:
            raise ValueError("Engine name required")
        self.engines[name] = engine

    def register_provider(self, name: str, provider: Any):
        if not name:
            raise ValueError("Provider name required")
        self.providers[name] = provider

    def get_module(self, name: str):
        return self.modules.get(name)

    def get_engine(self, name: str):
        return self.engines.get(name)

    def get_provider(self, name: str):
        return self.providers.get(name)

    def describe(self):
        return {
            "modules": sorted(self.modules),
            "engines": sorted(self.engines),
            "providers": sorted(self.providers),
        }
