# A2A – Agentic Mini (Planner + Executor with FastAPI and Ollama)

## Problem statement

Turn a user’s natural-language request into an orchestrated plan and an executed result. Baseline query: “Get the current weather in New York and give me a short summary.” The system must plan steps, execute tools, stream progress, and return a concise final answer.

## Architecture (layered)

- API (FastAPI): `POST /agent` (one-shot) and `POST /agent/stream` (NDJSON streaming)
- Domain
  - Agent A – Planner: parse query → emit tasks (`WeatherTask`, `SummaryTask`)
  - Agent B – Executor: run tasks via services (weather fetch, summarization)
  - Orchestrator: sequence Planner → Executor and aggregate outputs
- Services
  - `WeatherService` (Open‑Meteo geocoding + current weather → normalized dict)
  - `SummarizationService` (Ollama LLM; rule-based fallback)
- Core
  - `httpx` AsyncClient lifecycle, config, LLM helper

## Why this design

- Clear separation of concerns: plan vs do vs coordinate
- Hybrid AI/rules: rules for structure; AI for language quality (with fallback)
- Async + streaming: responsive UI and easy Postman/curl demos
- Extensible: add tools by adding a Service + Task and one Orchestrator step

## Run locally

Requirements: Python 3.13+, curl (optional), Ollama (optional)

```bash
# from repo root: /Users/sunilsastrinathsanaboina/Desktop/work/ai/A2A
bash scripts/dev.sh
cp .env.example .env    # optional; set OLLAMA_MODEL=mistral or llama3
bash scripts/run.sh     # starts on http://localhost:8000
```

## API

### One-shot

- POST `/agent`
- Body

```json
{ "query": "Get the current weather in New York and give me a short summary." }
```

- Response

```json
{
  "tasks": ["Get weather data for New York", "Summarize the weather data"],
  "intermediate": {
    "weather_raw": {
      "temp_c": 24.1,
      "desc": "clear sky",
      "humidity": 84,
      "wind_kph": 15,
      "coordinates": { "lat": 40.7, "lon": -74.0 }
    }
  },
  "final_summary": "New York: Clear sky, around 24°C, wind 15 km/h, humidity 84%."
}
```

### Streaming (NDJSON)

- POST `/agent/stream`
- Body same as above
- Response: newline-delimited JSON events (each line is a JSON object)

```text
{"agent":"Planner","status":"Planning"}
{"agent":"Planner","status":"Completed","output":["Get weather data for New York","Summarize the weather data"]}
{"agent":"Executor:Weather","status":"Fetching"}
{"agent":"Executor:Weather","status":"Completed","output":{...normalized weather...}}
{"agent":"Executor:Summary","status":"Summarizing"}
{"agent":"Executor:Summary","status":"Completed","output":"New York: ..."}
{"agent":"Orchestrator","status":"Completed","output":{...final payload...}}
```

Tip: test with curl

```bash
curl -N -X POST http://localhost:8000/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"query":"Get the current weather in New York and give me a short summary."}'
```

## Files to know

- `src/app/main.py`: FastAPI app, lifespan, CORS
- `src/app/api/v1/routes.py`: `/agent`, `/agent/stream`
- `src/app/api/v1/schemas.py`: request/response models
- `src/domain/agents/*`: planner, executor, orchestrator
- `src/domain/services/*`: weather and summarization services
- `src/core/*`: http client, settings, LLM helpers

## Extending

- Add a tool:
  1. Define `NewTask` (in `domain/tasks.py`)
  2. Implement `NewService` wrapping the external API
  3. Planner emits the new task; Executor adds a handler; Orchestrator streams a new step
- Scale-out options:
  - Multiple Uvicorn workers; containerize and use HPA
  - Introduce a message bus (Kafka/Redis Streams) for decoupled Planner/Executor workers
  - Add caching (geocode), retries/backoff, and circuit breakers
