from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.connection import get_session
from src.api.services.decisions import process_decisions_service
from src.api.schemas.decisions import DecisionRequest, DecisionResponse

router = APIRouter()

@router.post("/reasoning", response_model=list[DecisionResponse], status_code=status.HTTP_200_OK)
async def process_decisions_reasoning(
    payload: DecisionRequest,
    simulation_id: int = Query(..., description="Simulation ID to create decisions"),
    round_id: int = Query(..., description="Round ID to decisions"),
    session: AsyncSession = Depends(get_session)
):
    return await process_decisions_service(simulation_id, round_id, payload, session)