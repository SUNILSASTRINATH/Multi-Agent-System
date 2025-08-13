from typing import Any, Dict, Optional
from core.http import get_client

WMO_DESC = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "depositing rime fog",
    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
    56: "freezing drizzle", 57: "dense freezing drizzle",
    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
    66: "freezing rain", 67: "heavy freezing rain",
    71: "slight snow fall", 73: "moderate snow fall", 75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers", 81: "moderate rain showers", 82: "violent rain showers",
    85: "slight snow showers", 86: "heavy snow showers",
    95: "thunderstorm", 96: "thunderstorm with slight hail", 99: "thunderstorm with heavy hail",
}

class WeatherService:
    async def geocode(self, location: str) -> Optional[dict]:
        client = await get_client()
        r = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"},
        )
        r.raise_for_status()
        data = r.json()
        results = data.get("results") or []
        return results[0] if results else None

    async def get_current_weather(self, location: str) -> Dict[str, Any]:
        geo = await self.geocode(location)
        if not geo:
            return {"error": f"Could not geocode location {location}"}

        lat = geo["latitude"]
        lon = geo["longitude"]

        client = await get_client()
        r = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
                "wind_speed_unit": "kmh",
                "timezone": "auto",
            },
        )
        r.raise_for_status()
        data = r.json()
        current = (data.get("current") or {})
        code = current.get("weather_code")
        desc = WMO_DESC.get(code, "unknown conditions")

        normalized = {
            "provider": "open-meteo",
            "location": location,
            "coordinates": {"lat": lat, "lon": lon},
            "temp_c": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "precip_mm": current.get("precipitation", 0.0),
            "wind_kph": current.get("wind_speed_10m"),
            "weather_code": code,
            "desc": desc,
            "raw": current
        }
        return normalized
