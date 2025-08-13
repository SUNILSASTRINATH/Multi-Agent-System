from typing import Dict, Any
from domain.services.weather_service import WeatherService
from domain.services.summarization_service import SummarizationService

class AgentBExecutor:
    def __init__(self) -> None:
        self.weather_service = WeatherService()
        self.summarizer = SummarizationService()

    async def get_weather(self, location: str) -> Dict[str, Any]:
        return await self.weather_service.get_current_weather(location)

    async def summarize(self, weather: Dict[str, Any], location: str, user_query: str) -> str:
        return await self.summarizer.summarize(weather, location, user_query)
