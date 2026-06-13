from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.db.models import Simulation
from src.api.schemas.simulations import SimulationCreate, SimulationUpdate

async def create_simulation_service(
    sim_data: SimulationCreate, session: AsyncSession
) -> Simulation:
    simulation = Simulation(
        platform=sim_data.platform, 
        attributes=sim_data.attributes
    )
    session.add(simulation)
    await session.commit()
    await session.refresh(simulation)
    return simulation

async def list_simulations_service(session: AsyncSession) -> list[Simulation]:
    result = await session.execute(select(Simulation))
    return list(result.scalars().all())

async def update_simulation_service(
    simulation_id: int, 
    update_data: SimulationUpdate, 
    session: AsyncSession
) -> Simulation:
    
    result = await session.execute(
        select(Simulation).where(Simulation.simulation_id == simulation_id)
    )
    simulation = result.scalar_one_or_none()

    if not simulation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Simulation with id {simulation_id} not found."
        )

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(simulation, key, value)

    await session.commit()
    await session.refresh(simulation)
    
    return simulation