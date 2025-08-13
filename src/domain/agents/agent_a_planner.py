import re
from typing import List, Tuple
from domain.tasks import WeatherTask, SummaryTask

LOCATION_REGEX = re.compile(r"\bin\s+([A-Za-z\s]+?)(?:[.,;]| and\b|$)", flags=re.IGNORECASE)

def extract_location(user_query: str) -> str:
    m = LOCATION_REGEX.search(user_query)
    if m:
        loc = m.group(1).strip()
        return " ".join(loc.split())

    tokens = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", user_query)
    for t in tokens:
        if t.lower() not in {"get", "give", "weather", "current", "summary"}:
            return t.strip()

    return "New York"


def plan(user_query: str) -> Tuple[List[str], WeatherTask, SummaryTask]:
    location = extract_location(user_query)
    t1 = WeatherTask(description=f"Get weather data for {location}", location=location)
    t2 = SummaryTask(description="Summarize the weather data", location=location)
    tasks = [t1.description, t2.description]
    return tasks, t1, t2
