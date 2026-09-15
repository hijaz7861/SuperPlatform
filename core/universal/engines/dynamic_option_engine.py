
"""
SuperPlatform Universal Dynamic Option Engine

Purpose:
- Dynamically register options, fields, actions and workflows.
- Validate changes before activation.
- Version every configuration state.
- Support rollback.
- Enforce permissions/policies.
- Keep the engine provider-independent.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DynamicOption:
    key: str
    label: str
    value_type: str = "string"
    default: Any = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DynamicAction:
    key: str
    label: str
    enabled: bool = True
    approval_required: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DynamicField:
    key: str
    label: str
    value_type: str = "string"
    required: bool = False
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DynamicWorkflow:
    key: str
    label: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class OptionValidationError(ValueError):
    pass


class UniversalDynamicOptionEngine:

    VERSION = "1.0.0"

    def __init__(self):
        self.options: Dict[str, DynamicOption] = {}
        self.actions: Dict[str, DynamicAction] = {}
        self.fields: Dict[str, DynamicField] = {}
        self.workflows: Dict[str, DynamicWorkflow] = {}

        self.history: List[Dict[str, Any]] = []
        self.audit_log: List[Dict[str, Any]] = []

        self._save_version("initial")

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    @staticmethod
    def _valid_key(key: str) -> bool:
        if not isinstance(key, str):
            return False
        if not key or len(key) > 128:
            return False
        allowed = set("abcdefghijklmnopqrstuvwxyz"
                      "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                      "0123456789_-")
        return all(ch in allowed for ch in key)

    def validate_key(self, key: str):
        if not self._valid_key(key):
            raise OptionValidationError(
                f"Invalid dynamic key: {key!r}"
            )

    # --------------------------------------------------------
    # Audit
    # --------------------------------------------------------

    def _audit(self, event: str, target: str, details=None):
        self.audit_log.append({
            "id": str(uuid.uuid4()),
            "timestamp": utc_now(),
            "event": event,
            "target": target,
            "details": details or {},
        })

    # --------------------------------------------------------
    # Versioning
    # --------------------------------------------------------

    def _snapshot(self):
        return {
            "options": deepcopy(
                {k: asdict(v) for k, v in self.options.items()}
            ),
            "actions": deepcopy(
                {k: asdict(v) for k, v in self.actions.items()}
            ),
            "fields": deepcopy(
                {k: asdict(v) for k, v in self.fields.items()}
            ),
            "workflows": deepcopy(
                {k: asdict(v) for k, v in self.workflows.items()}
            ),
        }

    def _save_version(self, reason: str):
        self.history.append({
            "version": len(self.history) + 1,
            "timestamp": utc_now(),
            "reason": reason,
            "snapshot": self._snapshot(),
        })

    def version(self) -> int:
        return len(self.history)

    def rollback(self, version: int):
        if version < 1 or version > len(self.history):
            raise ValueError("Invalid rollback version")

        snapshot = self.history[version - 1]["snapshot"]

        self.options = {
            k: DynamicOption(**v)
            for k, v in snapshot["options"].items()
        }

        self.actions = {
            k: DynamicAction(**v)
            for k, v in snapshot["actions"].items()
        }

        self.fields = {
            k: DynamicField(**v)
            for k, v in snapshot["fields"].items()
        }

        self.workflows = {
            k: DynamicWorkflow(**v)
            for k, v in snapshot["workflows"].items()
        }

        self._audit(
            "rollback",
            "engine",
            {"target_version": version}
        )

    # --------------------------------------------------------
    # Dynamic Options
    # --------------------------------------------------------

    def add_option(
        self,
        key: str,
        label: str,
        value_type: str = "string",
        default: Any = None,
        metadata=None,
    ):
        self.validate_key(key)

        if key in self.options:
            raise OptionValidationError(
                f"Option already exists: {key}"
            )

        self.options[key] = DynamicOption(
            key=key,
            label=label,
            value_type=value_type,
            default=default,
            metadata=metadata or {},
        )

        self._audit("add_option", key)
        self._save_version(f"add_option:{key}")
        return self.options[key]

    def remove_option(self, key: str):
        if key not in self.options:
            raise KeyError(key)

        del self.options[key]
        self._audit("remove_option", key)
        self._save_version(f"remove_option:{key}")

    def enable_option(self, key: str):
        self.options[key].enabled = True
        self._audit("enable_option", key)
        self._save_version(f"enable_option:{key}")

    def disable_option(self, key: str):
        self.options[key].enabled = False
        self._audit("disable_option", key)
        self._save_version(f"disable_option:{key}")

    # --------------------------------------------------------
    # Dynamic Fields
    # --------------------------------------------------------

    def add_field(
        self,
        key: str,
        label: str,
        value_type: str = "string",
        required: bool = False,
        metadata=None,
    ):
        self.validate_key(key)

        if key in self.fields:
            raise OptionValidationError(
                f"Field already exists: {key}"
            )

        self.fields[key] = DynamicField(
            key=key,
            label=label,
            value_type=value_type,
            required=required,
            metadata=metadata or {},
        )

        self._audit("add_field", key)
        self._save_version(f"add_field:{key}")
        return self.fields[key]

    # --------------------------------------------------------
    # Dynamic Actions
    # --------------------------------------------------------

    def add_action(
        self,
        key: str,
        label: str,
        approval_required: bool = False,
        metadata=None,
    ):
        self.validate_key(key)

        if key in self.actions:
            raise OptionValidationError(
                f"Action already exists: {key}"
            )

        self.actions[key] = DynamicAction(
            key=key,
            label=label,
            approval_required=approval_required,
            metadata=metadata or {},
        )

        self._audit("add_action", key)
        self._save_version(f"add_action:{key}")
        return self.actions[key]

    # --------------------------------------------------------
    # Dynamic Workflows
    # --------------------------------------------------------

    def add_workflow(
        self,
        key: str,
        label: str,
        steps=None,
        metadata=None,
    ):
        self.validate_key(key)

        if key in self.workflows:
            raise OptionValidationError(
                f"Workflow already exists: {key}"
            )

        self.workflows[key] = DynamicWorkflow(
            key=key,
            label=label,
            steps=steps or [],
            metadata=metadata or {},
        )

        self._audit("add_workflow", key)
        self._save_version(f"add_workflow:{key}")
        return self.workflows[key]

    # --------------------------------------------------------
    # Export / Inspection
    # --------------------------------------------------------

    def export_schema(self):
        return {
            "engine": "UniversalDynamicOptionEngine",
            "version": self.VERSION,
            "config_version": self.version(),
            "options": {
                k: asdict(v)
                for k, v in self.options.items()
            },
            "fields": {
                k: asdict(v)
                for k, v in self.fields.items()
            },
            "actions": {
                k: asdict(v)
                for k, v in self.actions.items()
            },
            "workflows": {
                k: asdict(v)
                for k, v in self.workflows.items()
            },
        }

    def audit(self):
        return deepcopy(self.audit_log)
