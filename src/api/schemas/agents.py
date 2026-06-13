from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class AgentBase(BaseModel):
    attributes: Optional[dict[str, Any]] = None
    state: Optional[list[dict[str, Any]]] = None

class AgentCreate(AgentBase):
    agent_id: int

class AgentUpdate(AgentBase):
    agent_id: int

class AgentRead(AgentBase):
    simulation_id: int
    agent_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)