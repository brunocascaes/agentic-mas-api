from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class RoundBase(BaseModel):
    attributes: Optional[dict[str, Any]] = None

class RoundCreate(RoundBase):
    pass

class RoundUpdate(BaseModel):
    attributes: Optional[dict[str, Any]] = None
    metrics: Optional[dict[str, Any]] = None
    finished_at: Optional[datetime] = None

class RoundRead(RoundBase):
    simulation_id: int
    round_id: int
    created_at: datetime
    metrics: Optional[dict[str, Any]] = None
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)