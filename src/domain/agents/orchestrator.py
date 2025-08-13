from typing import Dict, Any
from app.api.v1.schemas import AgentResponse
from domain.agents.agent_a_planner import plan
from domain.agents.agent_b_executor import AgentBExecutor

class Orchestrator:
    def __init__(self) -> None:
        self.executor = AgentBExecutor()

    async def handle_query(self, user_query: str) -> AgentResponse:
        tasks_list, weather_task, summary_task = plan(user_query)

        intermediate: Dict[str, Any] = {}

        weather_data = await self.executor.get_weather(weather_task.location)
        intermediate["weather_raw"] = weather_data

        final_summary = await self.executor.summarize(weather_data, summary_task.location, user_query)

        return AgentResponse(
            tasks=tasks_list,
            intermediate=intermediate,
            final_summary=final_summary
        )
