"""Shared config loader for modules."""
import json
from pathlib import Path


def load_config(module_name, default=None):
    default = default or {}
    cfg_path = Path(__file__).resolve().parent / module_name / "config.json"
    if cfg_path.exists():
        try:
            return {**default, **json.loads(cfg_path.read_text())}
        except Exception:
            return default
    return default
