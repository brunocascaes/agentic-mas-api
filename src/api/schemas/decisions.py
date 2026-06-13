from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional

class DecisionRequest(BaseModel):
    type: str
    framework: str = Field(default="agno")
    config: dict[str, Any] = Field(default_factory=dict)
    context: list[dict[str, Any]] = Field(default_factory=list)

class DecisionResponse(BaseModel):
    simulation_id: int
    round_id: int
    agent_id: int
    response: list[Any]

    model_config = ConfigDict(from_attributes=True)
