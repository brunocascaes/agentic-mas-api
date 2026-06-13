from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.connection import get_session
from src.api.services.simulations import (
    create_simulation_service, list_simulations_service, update_simulation_service
)
from src.api.schemas.simulations import SimulationCreate, SimulationRead, SimulationUpdate

router = APIRouter()

@router.post("", response_model=SimulationRead, status_code=status.HTTP_201_CREATED)
async def create_simulation(simulation_data: SimulationCreate, session: AsyncSession = Depends(get_session)):
    return await create_simulation_service(simulation_data, session)

@router.get("", response_model=list[SimulationRead])
async def list_simulations(session: AsyncSession = Depends(get_session)):
    return await list_simulations_service(session)

@router.patch("/{simulation_id}", response_model=SimulationRead)
async def update_simulation(
    simulation_id: int,
    update_data: SimulationUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await update_simulation_service(simulation_id, update_data, session)
