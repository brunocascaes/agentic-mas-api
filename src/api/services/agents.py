from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.models import Agent
from src.api.schemas.agents import AgentCreate, AgentUpdate

async def create_agents_service(
    simulation_id: int, agents_data: list[AgentCreate], session: AsyncSession
) -> dict:
    agents = [
        Agent(
            simulation_id=simulation_id,
            agent_id=agent.agent_id,
            attributes=agent.attributes,
            state=agent.state if agent.state is not None else []
        ) for agent in agents_data
    ]
    session.add_all(agents)
    await session.commit()
    return {"created_agents_count": len(agents)}

async def get_agents_by_simulation_service(
    simulation_id: int, session: AsyncSession
) -> list[Agent]:
    result = await session.execute(
        select(Agent).where(Agent.simulation_id == simulation_id)
    )
    return list(result.scalars().all())

async def update_agents_service(
    simulation_id: int, 
    update_data: list[AgentUpdate], 
    session: AsyncSession
) -> dict:
    
    agent_ids = [item.agent_id for item in update_data]

    result = await session.execute(
        select(Agent).where(
            Agent.simulation_id == simulation_id,
            Agent.agent_id.in_(agent_ids)
        )
    )
    agents_map = {a.agent_id: a for a in result.scalars().all()}

    updated_count = 0

    for item in update_data:
        agent = agents_map.get(item.agent_id)
        if agent:
            update_dict = item.model_dump(exclude_unset=True, exclude={"agent_id"})
            
            for key, value in update_dict.items():
                if key == "state":
                    current_state = agent.state or []
                    
                    if not isinstance(current_state, list):
                        current_state = [current_state]
                        
                    new_state_list = list(current_state) 

                    if isinstance(value, list):
                        new_state_list.extend(value)
                    else:
                        new_state_list.append(value)
                        
                    setattr(agent, key, new_state_list)
                else:
                    setattr(agent, key, value)
            
            updated_count += 1

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No matching agents found for simulation {simulation_id}."
        )

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"status": "updated", "updated_count": updated_count}
