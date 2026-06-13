# src/api/routes/rounds.py

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.connection import get_session
from src.api.services.rounds import (
    create_round_service, get_rounds_by_simulation_service, update_round_service
)
from src.api.schemas.rounds import RoundCreate, RoundRead, RoundUpdate

router = APIRouter()

@router.post("", response_model=RoundRead, status_code=status.HTTP_201_CREATED)
async def create_round(
    round_data: RoundCreate,
    simulation_id: int = Query(..., description="Simulation ID to create rounds"),
    round_id: int = Query(..., description="Round ID to create"),
    session: AsyncSession = Depends(get_session)
):
    return await create_round_service(simulation_id, round_id, round_data, session)

@router.get("", response_model=list[RoundRead])
async def list_rounds(
    simulation_id: int = Query(..., description="Simulation ID to filter rounds"), 
    session: AsyncSession = Depends(get_session)
):
    return await get_rounds_by_simulation_service(simulation_id, session)

@router.patch("", response_model=dict)
async def update_round(
    update_data: RoundUpdate,
    simulation_id: int = Query(..., description="Simulation ID to update round"),
    round_id: int = Query(..., description="Round ID to update round"),
    session: AsyncSession = Depends(get_session)
):
    return await update_round_service(simulation_id, round_id, update_data, session)