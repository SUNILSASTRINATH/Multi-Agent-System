from typing import Dict
from core.llm import summarize_with_ollama, rule_based_summary

class SummarizationService:
    async def summarize(self, weather: Dict, location: str, user_query: str) -> str:
        prompt = (
            "Write a short, user-friendly weather summary.\n"
            f"Location: {location}\n"
            f"Data: {weather}\n"
            "Constraints: 1-2 sentences, concise, helpful, no extra fluff.\n"
        )
        system = "You are a helpful assistant that summarizes weather for non-experts."
        text = await summarize_with_ollama(prompt=prompt, system=system)
        if text:
            return text
        return rule_based_summary(weather, location)
