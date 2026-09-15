
from typing import Any, Callable, Dict, List
from uuid import uuid4

from core.agents.models.agent_models import (
    Agent,
    AgentTask,
)


class AgentEngine:

    def __init__(self, policy_engine=None):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, AgentTask] = {}
        self.handlers: Dict[str, Callable] = {}
        self.audit: List[Dict[str, Any]] = []
        self.policy_engine = policy_engine

    # --------------------------------------------------------
    # AGENTS
    # --------------------------------------------------------

    def register_agent(
        self,
        name: str,
        department: str,
        capabilities=None,
        metadata=None,
    ) -> Agent:

        if not name:
            raise ValueError("Agent name required")

        if not department:
            raise ValueError("Department required")

        agent_id = str(uuid4())

        agent = Agent(
            agent_id=agent_id,
            name=name,
            department=department,
            capabilities=capabilities or [],
            metadata=metadata or {},
        )

        self.agents[agent_id] = agent

        self._audit(
            "agent_registered",
            agent_id,
            {
                "name": name,
                "department": department,
            },
        )

        return agent

    def disable_agent(self, agent_id: str):
        agent = self.agents[agent_id]
        agent.enabled = False
        agent.status = "disabled"

        self._audit(
            "agent_disabled",
            agent_id,
        )

    def enable_agent(self, agent_id: str):
        agent = self.agents[agent_id]
        agent.enabled = True
        agent.status = "idle"

        self._audit(
            "agent_enabled",
            agent_id,
        )

    def find_agents(
        self,
        department: str,
        capability: str | None = None,
    ) -> List[Agent]:

        results = []

        for agent in self.agents.values():

            if not agent.enabled:
                continue

            if agent.department != department:
                continue

            if capability and capability not in agent.capabilities:
                continue

            results.append(agent)

        return results

    # --------------------------------------------------------
    # TASKS
    # --------------------------------------------------------

    def create_task(
        self,
        title: str,
        department: str,
        requested_by: str = "system",
        priority: int = 50,
        approval_required: bool = False,
    ) -> AgentTask:

        if not title:
            raise ValueError("Task title required")

        task = AgentTask(
            task_id=str(uuid4()),
            title=title,
            department=department,
            requested_by=requested_by,
            priority=priority,
            approval_required=approval_required,
        )

        self.tasks[task.task_id] = task

        self._audit(
            "task_created",
            task.task_id,
            {
                "department": department,
                "approval_required": approval_required,
            },
        )

        return task

    def assign_task(
        self,
        task_id: str,
        agent_id: str,
    ):

        task = self.tasks[task_id]
        agent = self.agents[agent_id]

        if not agent.enabled:
            raise RuntimeError("Agent is disabled")

        if task.department != agent.department:
            raise ValueError(
                "Agent department does not match task"
            )

        task.assigned_agent = agent_id
        task.status = "assigned"
        task.updated_at = self._now()

        agent.status = "working"

        self._audit(
            "task_assigned",
            task_id,
            {"agent_id": agent_id},
        )

        return task

    # --------------------------------------------------------
    # EXECUTION
    # --------------------------------------------------------

    def register_handler(
        self,
        capability: str,
        handler: Callable,
    ):
        if not callable(handler):
            raise TypeError("Handler must be callable")

        self.handlers[capability] = handler

    def execute(
        self,
        task_id: str,
        capability: str,
        payload: Any = None,
        approval_granted: bool = False,
    ):

        task = self.tasks[task_id]

        if task.approval_required and not approval_granted:
            task.status = "awaiting_approval"

            self._audit(
                "approval_required",
                task_id,
            )

            return {
                "status": "awaiting_approval",
                "executed": False,
            }

        if not task.assigned_agent:
            raise RuntimeError("Task has no assigned agent")

        agent = self.agents[task.assigned_agent]

        if capability not in agent.capabilities:
            raise PermissionError(
                "Agent lacks requested capability"
            )

        if capability not in self.handlers:
            raise RuntimeError(
                f"No handler registered for capability: {capability}"
            )

        task.status = "running"
        agent.status = "working"

        try:
            result = self.handlers[capability](payload)

            task.result = result
            task.status = "completed"
            task.evidence = {
                "capability": capability,
                "handler_registered": True,
                "execution_confirmed": True,
            }

            agent.status = "idle"

            self._audit(
                "task_completed",
                task_id,
                {
                    "agent_id": agent.agent_id,
                    "capability": capability,
                },
            )

            return {
                "status": "completed",
                "executed": True,
                "result": result,
                "evidence": task.evidence,
            }

        except Exception as exc:

            task.status = "failed"
            task.evidence = {
                "execution_confirmed": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }

            agent.status = "idle"

            self._audit(
                "task_failed",
                task_id,
                task.evidence,
            )

            raise

    # --------------------------------------------------------
    # DELEGATION
    # --------------------------------------------------------

    def delegate(
        self,
        task_id: str,
        target_department: str,
        title: str | None = None,
    ):

        parent = self.tasks[task_id]

        delegated = self.create_task(
            title=title or f"Delegated: {parent.title}",
            department=target_department,
            requested_by=parent.assigned_agent or "agent",
            priority=parent.priority,
        )

        self._audit(
            "task_delegated",
            task_id,
            {
                "child_task": delegated.task_id,
                "target_department": target_department,
            },
        )

        return delegated

    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    def health(self):

        enabled = [
            a for a in self.agents.values()
            if a.enabled
        ]

        return {
            "agents_total": len(self.agents),
            "agents_enabled": len(enabled),
            "tasks_total": len(self.tasks),
            "tasks_completed": sum(
                t.status == "completed"
                for t in self.tasks.values()
            ),
            "tasks_failed": sum(
                t.status == "failed"
                for t in self.tasks.values()
            ),
        }

    # --------------------------------------------------------
    # INTERNAL
    # --------------------------------------------------------

    @staticmethod
    def _now():
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def _audit(self, event, target, details=None):
        self.audit.append({
            "event": event,
            "target": target,
            "details": details or {},
            "timestamp": self._now(),
        })
