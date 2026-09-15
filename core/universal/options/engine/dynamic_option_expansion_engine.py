from copy import deepcopy

from ..models.option_models import (
    DynamicOption,
    OptionAudit,
    OptionVersion,
)


class DynamicOptionExpansionEngine:

    def __init__(self):
        self.options = {}
        self.history = {}
        self.audit_log = []

    def add_option(
        self,
        option_id,
        name,
        value_type="string",
        default=None,
        metadata=None,
    ):
        if option_id in self.options:
            raise ValueError(f"Option already exists: {option_id}")

        option = DynamicOption(
            option_id=option_id,
            name=name,
            value_type=value_type,
            default=default,
            metadata=dict(metadata or {}),
        )

        self.options[option_id] = option
        self._snapshot(option)

        self._audit(
            "ADD",
            option_id,
            option.version,
        )

        return option

    def update_option(self, option_id, **changes):
        option = self._require(option_id)

        allowed = {
            "name",
            "value_type",
            "default",
            "metadata",
        }

        for key in changes:
            if key not in allowed:
                raise ValueError(f"Unsupported option field: {key}")

        for key, value in changes.items():
            setattr(option, key, value)

        option.version += 1
        self._snapshot(option)

        self._audit(
            "UPDATE",
            option_id,
            option.version,
        )

        return option

    def enable_option(self, option_id):
        option = self._require(option_id)
        option.enabled = True
        option.version += 1
        self._snapshot(option)
        self._audit("ENABLE", option_id, option.version)
        return option

    def disable_option(self, option_id):
        option = self._require(option_id)
        option.enabled = False
        option.version += 1
        self._snapshot(option)
        self._audit("DISABLE", option_id, option.version)
        return option

    def get_option(self, option_id):
        return self._require(option_id)

    def list_options(self, enabled_only=False):
        values = list(self.options.values())
        if enabled_only:
            values = [x for x in values if x.enabled]
        return values

    def rollback(self, option_id, version):
        option = self._require(option_id)

        snapshots = self.history.get(option_id, [])

        target = next(
            (
                item
                for item in snapshots
                if item.version == version
            ),
            None,
        )

        if target is None:
            raise ValueError(
                f"Option version not found: {option_id}@{version}"
            )

        restored = deepcopy(target.snapshot)

        option.name = restored["name"]
        option.value_type = restored["value_type"]
        option.default = restored["default"]
        option.enabled = restored["enabled"]
        option.metadata = restored["metadata"]
        option.version = restored["version"]

        self._audit(
            "ROLLBACK",
            option_id,
            option.version,
        )

        return option

    def _snapshot(self, option):
        snapshot = {
            "name": option.name,
            "value_type": option.value_type,
            "default": deepcopy(option.default),
            "enabled": option.enabled,
            "metadata": deepcopy(option.metadata),
            "version": option.version,
        }

        self.history.setdefault(
            option.option_id,
            [],
        ).append(
            OptionVersion(
                option_id=option.option_id,
                version=option.version,
                snapshot=snapshot,
            )
        )

    def _audit(self, action, option_id, version):
        self.audit_log.append(
            OptionAudit(
                action=action,
                option_id=option_id,
                version=version,
            )
        )

    def _require(self, option_id):
        if option_id not in self.options:
            raise KeyError(
                f"Unknown option: {option_id}"
            )
        return self.options[option_id]
