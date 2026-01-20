from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_coingecko_client, get_price_cache
from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.schemas.crypto import CryptoPriceResponse
from app.services.crypto_service import CryptoService

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/{symbol}/price", response_model=CryptoPriceResponse)
async def get_crypto_price(
    symbol: str,
    client: CoinGeckoClient = Depends(get_coingecko_client),
    cache: InMemoryCache = Depends(get_price_cache),
) -> CryptoPriceResponse:
    service = CryptoService(client, cache)

    try:
        price = await service.get_current_price(symbol)
    except Exception as err:
        raise HTTPException(
            status_code=404,
            detail="Crypto not found",
        ) from err

    return CryptoPriceResponse(
        symbol=symbol.upper(),
        price_usd=price,
    )
