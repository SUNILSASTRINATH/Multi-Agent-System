from dataclasses import dataclass

@dataclass
class Task:
    description: str

@dataclass
class WeatherTask(Task):
    location: str

@dataclass
class SummaryTask(Task):
    location: str
