from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import json
from app.api.v1.schemas import AgentQuery, AgentResponse
from domain.agents.orchestrator import Orchestrator
from domain.agents.agent_a_planner import plan
from domain.agents.agent_b_executor import AgentBExecutor

router = APIRouter()

@router.post("/agent", response_model=AgentResponse)
async def handle_agent(query: AgentQuery) -> AgentResponse:
    try:
        orchestrator = Orchestrator()
        return await orchestrator.handle_query(query.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/stream")
async def handle_agent_stream(query: AgentQuery) -> StreamingResponse:
    async def event_gen():
        try:
            # Planner
            yield json.dumps({"agent": "Planner", "status": "Planning"}) + "\n"
            tasks_list, weather_task, summary_task = plan(query.query)
            await asyncio.sleep(0.1)
            yield json.dumps({"agent": "Planner", "status": "Completed", "output": tasks_list}) + "\n"

            # Executor: weather fetch
            executor = AgentBExecutor()
            yield json.dumps({"agent": "Executor:Weather", "status": "Fetching"}) + "\n"
            weather_data = await executor.get_weather(weather_task.location)
            await asyncio.sleep(0.1)
            yield json.dumps({"agent": "Executor:Weather", "status": "Completed", "output": weather_data}) + "\n"

            # Executor: summarization
            yield json.dumps({"agent": "Executor:Summary", "status": "Summarizing"}) + "\n"
            final_summary = await executor.summarize(weather_data, summary_task.location, query.query)
            await asyncio.sleep(0.1)
            yield json.dumps({"agent": "Executor:Summary", "status": "Completed", "output": final_summary}) + "\n"

            # Final
            final_payload = {
                "tasks": tasks_list,
                "intermediate": {"weather_raw": weather_data},
                "final_summary": final_summary,
            }
            yield json.dumps({"agent": "Orchestrator", "status": "Completed", "output": final_payload}) + "\n"
        except Exception as e:
            yield json.dumps({"agent": "Orchestrator", "status": "Error", "output": str(e)}) + "\n"

    return StreamingResponse(event_gen(), media_type="application/x-ndjson")
