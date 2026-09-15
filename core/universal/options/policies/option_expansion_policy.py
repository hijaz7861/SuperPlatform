class OptionExpansionPolicy:

    def __init__(self, allow_dynamic=True):
        self.allow_dynamic = bool(allow_dynamic)

    def can_modify(self):
        return self.allow_dynamic

    def validate(self, option):
        if not option.option_id:
            raise ValueError("option_id is required")

        if not option.name:
            raise ValueError("option name is required")

        return True
