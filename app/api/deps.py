from fastapi import Request

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache


def get_coingecko_client(request: Request) -> CoinGeckoClient:
    return request.app.state.coingecko_client


def get_price_cache(request: Request) -> InMemoryCache:
    return request.app.state.price_cache
