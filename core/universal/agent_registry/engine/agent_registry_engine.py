
from ..models.registry_models import AgentRecord


class AgentRegistry:

    def __init__(self):
        self.agents = {}

    def register(self, agent_id, department, capability):
        agent = AgentRecord(
            agent_id=agent_id,
            department=department,
            capability=capability,
        )
        self.agents[agent_id] = agent
        return agent

    def disable(self, agent_id):
        self.agents[agent_id].enabled = False

    def find(self, capability):
        return [
            a for a in self.agents.values()
            if a.enabled and a.capability == capability
        ]
