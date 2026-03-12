import logging
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache

logger = logging.getLogger("coingecko")

MARKET_CACHE_TTL_SECONDS = 60
HISTORY_CACHE_TTL_SECONDS = 600
COINS_CACHE_TTL_SECONDS = 21600


@asynccontextmanager
async def lifespan(app: FastAPI):
    pro_api_key = os.getenv("COINGECKO_PRO_API_KEY")
    demo_api_key = os.getenv("COINGECKO_DEMO_API_KEY")

    headers: dict[str, str] = {}
    if pro_api_key:
        headers["x-cg-pro-api-key"] = pro_api_key
        logger.info("coingecko client configured with pro api key")
    elif demo_api_key:
        headers["x-cg-demo-api-key"] = demo_api_key
        logger.info("coingecko client configured with demo api key")
    else:
        logger.warning("coingecko api key not configured; requests may be rate-limited")

    http_client = httpx.AsyncClient(timeout=10.0, headers=headers or None)

    app.state.coingecko_client = CoinGeckoClient(http_client)
    app.state.market_cache = InMemoryCache(ttl_seconds=MARKET_CACHE_TTL_SECONDS)
    app.state.history_cache = InMemoryCache(ttl_seconds=HISTORY_CACHE_TTL_SECONDS)
    app.state.coins_cache = InMemoryCache(ttl_seconds=COINS_CACHE_TTL_SECONDS)

    yield

    await http_client.aclose()
