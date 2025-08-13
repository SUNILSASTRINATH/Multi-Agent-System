import httpx
from typing import Optional

_client: Optional[httpx.AsyncClient] = None

async def init_http() -> None:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(15.0, connect=10.0))

async def get_client() -> httpx.AsyncClient:
    if _client is None:
        await init_http()
    assert _client is not None
    return _client

async def shutdown_http() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
