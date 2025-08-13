from typing import Any, Dict, List
from pydantic import BaseModel, Field

class AgentQuery(BaseModel):
    query: str = Field(..., examples=["Get the current weather in New York and give me a short summary."])

class AgentResponse(BaseModel):
    tasks: List[str]
    intermediate: Dict[str, Any]
    final_summary: str
