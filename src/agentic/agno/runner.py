from typing import Any
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from src.agentic.base_runner import BaseAgentRunner
from src.config.settings import settings
import json
import re

def define_llm_model(llm_api: str, llm_model: str):
    if llm_api == "gemini":
        return Gemini(id=llm_model, api_key=settings.GOOGLE_API_KEY)

    if llm_api == "openai":
        return OpenAIChat(id=llm_model, api_key=settings.OPENAI_API_KEY)

    raise ValueError(f"Unsupported LLM provider: {llm_api}")


class AgnoRunner(BaseAgentRunner):

    async def run(
        self,
        config: dict,
        agent_context: list[dict],
        round_context: Any,
        simulation_context: Any
    ) -> dict:

        llm_api = config.get("llm_api", "OpenAI")
        llm_model = config.get("llm_model", "gpt-4.o-mini")
        enable_agentic_memory = config.get("enable_agentic_memory", False)

        db = None

        if enable_agentic_memory:
            db = PostgresDb(
                db_url=settings.DB_URL_ASYNCPG,
                db_schema="agentic_mas",
                memory_table="memories"
            )

        results = []

        for agent in agent_context:
            user_id = None

            if enable_agentic_memory:
                user_id = (
                    f"{simulation_context['simulation_id']}:"
                    f"{agent['agent_id']}"
                )

            decision_agent = Agent(
                model=define_llm_model(llm_api, llm_model),
                db=db,
                enable_agentic_memory=enable_agentic_memory,
                description="""
                    You are a simulation agent.
                    Make decisions based on the agent profile, simulation context and round context.
                """,
                instructions="""
                    Analyze all provided information.
                    Output ONLY valid JSON.
                    {
                        "action": "MOVE" | "WAIT",
                        "reasoning": "<short explanation>"
                    }
                """,
            )

            prompt = f"""
                AGENT PROFILE
                {json.dumps(agent.get("attributes", {}), indent=2)}

                ROUND CONTEXT
                {json.dumps(round_context, indent=2)}

                SIMULATION CONTEXT
                {json.dumps(simulation_context, indent=2)}

                Decide whether the agent should MOVE or WAIT.
            """

            try:
                response = await decision_agent.arun(prompt, user_id=user_id)

                clean = re.sub(
                    r"```json|```",
                    "",
                    response.content
                ).strip()

                content = json.loads(clean)

                results.append(
                    {
                        "agent_id": agent["agent_id"],
                        "response": content,
                        "status": "success",
                    }
                )

            except Exception as e:
                results.append(
                    {
                        "agent_id": agent["agent_id"],
                        "response": {
                            "action": "WAIT",
                            "reasoning": str(e),
                        },
                        "status": "error",
                    }
                )

        return {
            "results": results
        }