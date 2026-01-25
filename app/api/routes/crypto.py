from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_coingecko_client, get_price_cache
from app.api.deps_auth import get_current_user
from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.schemas.crypto import CryptoMarketResponse, CryptoPriceResponse, CryptoSummaryResponse
from app.services.crypto_service import CryptoService

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/{symbol}/price", response_model=CryptoPriceResponse)
async def get_crypto_price(
    symbol: str,
    user: str = Depends(get_current_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
    cache: InMemoryCache = Depends(get_price_cache),
) -> CryptoPriceResponse:
    service = CryptoService(client, cache)

    try:
        result = await service.get_current_price(symbol)
    except Exception as err:
        raise HTTPException(status_code=404, detail="Crypto not found") from err

    return CryptoPriceResponse(
        symbol=symbol.upper(),
        price_usd=result.price,
        cached=result.cached,
        last_updated=result.last_updated,
    )


@router.get("/{symbol}/summary", response_model=CryptoSummaryResponse)
async def get_crypto_summary(
    symbol: str,
    user: str = Depends(get_current_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
    cache: InMemoryCache = Depends(get_price_cache),
) -> CryptoSummaryResponse:
    service = CryptoService(client, cache)

    try:
        result = await service.get_current_price(symbol)
    except Exception as err:
        raise HTTPException(status_code=404, detail="Crypto not found") from err

    return CryptoSummaryResponse(
        symbol=symbol.upper(),
        price_usd=result.price,
        cached=result.cached,
        last_updated=result.last_updated,
    )


@router.get("/coins")
async def list_coins(
    user: str = Depends(get_current_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
):
    service = CryptoService(client, cache=None)
    return await service.list_supported_coins()


@router.get("/{symbol}/market", response_model=CryptoMarketResponse)
async def get_crypto_market(
    symbol: str,
    user: str = Depends(get_current_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
    cache: InMemoryCache = Depends(get_price_cache),
) -> CryptoMarketResponse:
    service = CryptoService(client, cache)

    try:
        result = await service.get_market_summary(symbol)
    except Exception as err:
        raise HTTPException(status_code=404, detail="Crypto not found") from err

    return CryptoMarketResponse(
        symbol=symbol.upper(),
        price_usd=result.price_usd,
        price_change_24h=result.price_change_24h,
        price_change_percentage_24h=result.price_change_percentage_24h,
        market_cap_usd=result.market_cap_usd,
        volume_24h_usd=result.volume_24h_usd,
        cached=result.cached,
        last_updated=result.last_updated,
    )
