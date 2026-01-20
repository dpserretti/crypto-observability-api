from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache


class CryptoService:
    def __init__(
        self,
        client: CoinGeckoClient,
        cache: InMemoryCache,
    ) -> None:
        self._client = client
        self._cache = cache

    async def get_current_price(self, symbol: str) -> float:
        cache_key = f"price:{symbol.lower()}"

        cached_price = self._cache.get(cache_key)
        if cached_price is not None:
            return cached_price

        coin_id = symbol.lower()
        price = await self._client.get_price(coin_id, "usd")

        self._cache.set(cache_key, price)

        return price
