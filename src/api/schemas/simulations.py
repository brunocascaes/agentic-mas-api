from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class SimulationBase(BaseModel):
    platform: str
    attributes: Optional[Dict[str, Any]] = None

class SimulationCreate(SimulationBase):
    pass

class SimulationUpdate(BaseModel):
    platform: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    finished_at: Optional[datetime] = None

class SimulationRead(SimulationBase):
    simulation_id: int
    created_at: datetime
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)