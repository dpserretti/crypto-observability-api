from fastapi import APIRouter, Depends

from app.api.deps import get_coingecko_client, get_market_cache
from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.schemas.crypto import CryptoCoinResponse, CryptoMarketResponse
from app.services.crypto_service import CryptoService

router = APIRouter(
    prefix="/crypto",
    tags=["crypto"],
)


@router.get("/coins", response_model=list[CryptoCoinResponse])
async def list_coins(
    client: CoinGeckoClient = Depends(get_coingecko_client),
):
    service = CryptoService(client=client, cache=None)
    return await service.list_supported_coins()


@router.get("/{symbol}", response_model=CryptoMarketResponse)
async def get_market(
    symbol: str,
    client: CoinGeckoClient = Depends(get_coingecko_client),
    cache: InMemoryCache = Depends(get_market_cache),
):
    service = CryptoService(client=client, cache=cache)
    return await service.get_market_summary(symbol)
