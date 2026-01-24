from datetime import datetime

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.services.models import CryptoPriceResult


class CryptoService:
    def __init__(
        self,
        client: CoinGeckoClient,
        cache: InMemoryCache,
    ) -> None:
        self._client = client
        self._cache = cache

    async def get_current_price(self, symbol: str) -> CryptoPriceResult:
        cache_key = f"price:{symbol.lower()}"

        cached = self._cache.get(cache_key)
        if cached is not None:
            return CryptoPriceResult(
                price=cached["value"],
                cached=True,
                last_updated=cached["timestamp"],
            )

        price = await self._client.get_price(symbol.lower(), "usd")

        self._cache.set(cache_key, price)

        return CryptoPriceResult(
            price=price,
            cached=False,
            last_updated=datetime.utcnow(),
        )
