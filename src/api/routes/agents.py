from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.connection import get_session
from src.api.services.agents import (
    create_agents_service, get_agents_by_simulation_service, update_agents_service
)
from src.api.schemas.agents import AgentCreate, AgentRead, AgentUpdate

router = APIRouter()

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_agents(
    agents_data: list[AgentCreate],
    simulation_id: int = Query(..., description="Simulation ID to create agents"),
    session: AsyncSession = Depends(get_session)
):
    return await create_agents_service(simulation_id, agents_data, session)

@router.get("", response_model=list[AgentRead])
async def list_agents(
    simulation_id: int = Query(..., description="Simulation ID to filter agents"), 
    session: AsyncSession = Depends(get_session)
):
    return await get_agents_by_simulation_service(simulation_id, session)

@router.patch("", response_model=dict)
async def update_agents(
    update_data: list[AgentUpdate],
    simulation_id: int = Query(..., description="Simulation ID to update agents"),
    session: AsyncSession = Depends(get_session)
):
    return await update_agents_service(simulation_id, update_data, session)