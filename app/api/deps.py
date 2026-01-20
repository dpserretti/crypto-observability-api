from fastapi import Request

from app.clients.coingecko import CoinGeckoClient


def get_coingecko_client(request: Request) -> CoinGeckoClient:
    return request.app.state.coingecko_client
