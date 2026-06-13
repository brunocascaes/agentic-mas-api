from src.agentic.base_runner import BaseAgentRunner
from src.agentic.agno.runner import AgnoRunner

def get_agent_runner(framework_name: str) -> BaseAgentRunner:
    runners = {
        "agno": AgnoRunner(),
    }
    
    runner = runners.get(framework_name.lower())
    if not runner:
        raise ValueError(f"Framework '{framework_name}' no available.")
    
    return runner