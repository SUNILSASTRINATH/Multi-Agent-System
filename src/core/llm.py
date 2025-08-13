import os
import asyncio
from typing import Optional

try:
    import ollama  # type: ignore
except Exception:
    ollama = None  # fallback

from core.config import settings

async def summarize_with_ollama(prompt: str, system: Optional[str] = None) -> Optional[str]:
    if ollama is None:
        return None

    model = settings.OLLAMA_MODEL or "mistral"
    host = settings.OLLAMA_HOST
    if host:
        os.environ["OLLAMA_HOST"] = host
    print(f"Using Ollama model: {model} on host: {host}")
    def _call() -> Optional[str]:
        try:
            resp = ollama.chat(model=model, messages=[
                {"role": "system", "content": system or "You are a helpful assistant that writes concise summaries."},
                {"role": "user", "content": prompt},
            ])
            content = resp.get("message", {}).get("content", "")
            return content.strip() if content else None
        except Exception:
            return None

    return await asyncio.to_thread(_call)


def rule_based_summary(weather: dict, location: str) -> str:
    parts = []
    temp = weather.get("temp_c")
    desc = weather.get("desc")
    humidity = weather.get("humidity")
    wind_kph = weather.get("wind_kph")
    precip_mm = weather.get("precip_mm")

    if desc:
        parts.append(desc.capitalize())
    if temp is not None:
        parts.append(f"around {round(temp)}°C")
    if wind_kph is not None:
        parts.append(f"wind {round(wind_kph)} km/h")
    if humidity is not None:
        parts.append(f"humidity {humidity}%")
    if precip_mm is not None and precip_mm > 0:
        parts.append("precipitation expected")

    core = ", ".join(parts) if parts else "Weather data unavailable"
    return f"{location}: {core}."
