class SecurityPolicy:

    def __init__(self):
        self.destructive_actions = False
        self.external_execution = False

        self.blocked = {
            "delete_system",
            "format_disk",
            "credential_theft",
            "unauthorized_access",
        }

    def allowed(self, action):
        if action in self.blocked:
            return False

        if action == "external_execution":
            return self.external_execution

        return True
