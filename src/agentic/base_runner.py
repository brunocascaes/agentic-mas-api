from abc import ABC, abstractmethod
from typing import Any
from typing import TypedDict

class AgentResult(TypedDict):
    agent_id: int
    response: str
    status: str

class BaseAgentRunner(ABC):

    @abstractmethod
    async def run(
        self,
        config: dict,
        agent_context: list[dict],
        round_context: dict,
        simulation_context: dict
    ) -> list[AgentResult]:
        pass