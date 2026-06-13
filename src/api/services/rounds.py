from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.models import Round
from src.api.schemas.rounds import RoundCreate, RoundUpdate

async def create_round_service(
    simulation_id: int, round_id: int, round_data: RoundCreate, session: AsyncSession
) -> Round:
    round = Round(
        simulation_id=simulation_id,
        round_id=round_id,
        attributes=round_data.attributes
    )
    session.add(round)
    await session.commit()
    await session.refresh(round)
    return round

async def get_rounds_by_simulation_service(
    simulation_id: int, session: AsyncSession
) -> list[Round]:
    result = await session.execute(
        select(Round).where(Round.simulation_id == simulation_id)
    )
    return list(result.scalars().all())

async def update_round_service(
    simulation_id: int, 
    round_id: int, 
    update_data: RoundUpdate, 
    session: AsyncSession
) -> dict:
    
    result = await session.execute(
        select(Round).where(
            Round.simulation_id == simulation_id,
            Round.round_id == round_id
        )
    )
    round_obj = result.scalar_one_or_none()

    if not round_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Round {round_id} not found for simulation {simulation_id}."
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(round_obj, key, value)

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"status": "updated", "round_id": round_id}
