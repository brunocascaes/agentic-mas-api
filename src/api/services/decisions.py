from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime
from src.db.models import Decision, Agent, Simulation, Round
from src.api.schemas.decisions import DecisionRequest
from src.agentic.factory import get_agent_runner

async def process_decisions_service(
    simulation_id: int, round_id: int, payload: DecisionRequest, session: AsyncSession
) -> list[dict]:
    
    created_at = datetime.utcnow()

    agent_ids = [
        item.get("agent_id") for item in payload.context if item.get("agent_id") is not None
    ]
    
    agents_result = await session.execute(
        select(Agent).where(
            Agent.simulation_id == simulation_id,
            Agent.agent_id.in_(agent_ids)
        )
    )
    agents_map = {agent.agent_id: agent for agent in agents_result.scalars().all()}

    agent_context = []
    for item in payload.context:
        agent_id = item.get("agent_id")
        agent_obj = agents_map.get(agent_id)
        
        enriched_item = dict(item)
        
        if agent_obj:
            enriched_item["attributes"] = agent_obj.attributes
            
        agent_context.append(enriched_item)

    simulation = await session.get(Simulation, simulation_id)

    simulation_context = {
        "id": simulation.simulation_id,
        "attributes": simulation.attributes
    }

    round_result = await session.execute(
        select(Round).where(
            Round.simulation_id == simulation_id,
            Round.round_id == round_id
        )
    )
    round = round_result.scalar_one()

    round_context = {
        "id": round.round_id,
        "attributes": round.attributes,
    }

    runner = get_agent_runner(payload.framework)
    
    runner_results = await runner.run(
        config=payload.config,
        agent_context=agent_context,
        round_context=round_context,
        simulation_context=simulation_context
    )
    
    context_map = {
        c["agent_id"]: c
        for c in payload.context
        if c.get("agent_id") is not None
    }

    decisions = []

    for result in runner_results["results"]:
        agent_id = result["agent_id"]

        decisions.append(
            Decision(
                simulation_id=simulation_id,
                round_id=round_id,
                agent_id=agent_id,
                framework=payload.framework,
                type=payload.type,
                config=payload.config,
                context=context_map.get(agent_id, {}),
                response=result.get("response"),
                status=result.get("status"),
                created_at=created_at,
                finished_at=func.now(),
            )
        )
    
    session.add_all(decisions)
    await session.commit()
    
    result = await session.execute(
        select(Decision).where(
            Decision.simulation_id == simulation_id,
            Decision.round_id == round_id,
            Decision.agent_id.in_(agent_ids)
        )
    )
    
    recent_decisions = list(result.scalars().all())
    
    formatted_decisions = []
    for dec in recent_decisions:
        formatted_decisions.append({
            "simulation_id": dec.simulation_id,
            "round_id": dec.round_id,
            "agent_id": dec.agent_id,
            "response": [dec.response]
        })

    return formatted_decisions