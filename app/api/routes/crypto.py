from fastapi import APIRouter, HTTPException

from app.clients.coingecko import CoinGeckoClient
from app.schemas.crypto import CryptoPriceResponse
from app.services.crypto_service import CryptoService

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/{symbol}/price", response_model=CryptoPriceResponse)
async def get_crypto_price(symbol: str) -> CryptoPriceResponse:
    client = CoinGeckoClient()
    service = CryptoService(client)

    try:
        price = await service.get_current_price(symbol)
    except Exception as err:
        raise HTTPException(status_code=404, detail="Crypto not found") from err
    finally:
        await client.close()

    return CryptoPriceResponse(
        symbol=symbol.upper(),
        price_usd=price,
    )
