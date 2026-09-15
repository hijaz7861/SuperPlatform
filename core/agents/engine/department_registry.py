
class DepartmentRegistry:

    def __init__(self):
        self.departments = {}

    def register(
        self,
        name,
        description="",
        metadata=None,
    ):
        if not name:
            raise ValueError("Department name required")

        self.departments[name] = {
            "name": name,
            "description": description,
            "metadata": metadata or {},
            "enabled": True,
        }

    def enable(self, name):
        self.departments[name]["enabled"] = True

    def disable(self, name):
        self.departments[name]["enabled"] = False

    def get(self, name):
        return self.departments.get(name)

    def list_enabled(self):
        return [
            d for d in self.departments.values()
            if d["enabled"]
        ]
