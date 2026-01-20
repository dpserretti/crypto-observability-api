from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client = httpx.AsyncClient(timeout=10.0)

    app.state.coingecko_client = CoinGeckoClient(http_client)
    app.state.price_cache = InMemoryCache(ttl_seconds=30)

    yield

    await http_client.aclose()
