from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as api_router
from core.http import init_http, shutdown_http


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_http()
    try:
        yield
    finally:
        await shutdown_http()


app = FastAPI(title="Agentic Mini", version="0.1.0", lifespan=lifespan)

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
