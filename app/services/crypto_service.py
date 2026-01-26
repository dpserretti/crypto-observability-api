from datetime import datetime

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.services.models import CryptoMarketResult


class CryptoService:
    def __init__(
        self,
        client: CoinGeckoClient,
        cache: InMemoryCache,
    ) -> None:
        self._client = client
        self._cache = cache

    async def list_supported_coins(self) -> list[dict]:
        return await self._client.list_coins()

    async def get_market_summary(self, symbol: str) -> CryptoMarketResult:
        cache_key = f"market:{symbol.lower()}"

        cached = self._cache.get(cache_key)
        if cached:
            return CryptoMarketResult(
                **cached["value"],
                cached=True,
            )

        data = await self._client.get_market_data(symbol.lower())
        market = data["market_data"]

        result = CryptoMarketResult(
            price_usd=market["current_price"]["usd"],
            price_change_24h=market["price_change_24h"],
            price_change_percentage_24h=market["price_change_percentage_24h"],
            market_cap_usd=market["market_cap"]["usd"],
            volume_24h_usd=market["total_volume"]["usd"],
            cached=False,
            last_updated=datetime.utcnow(),
        )

        self._cache.set(
            cache_key,
            {
                "price_usd": result.price_usd,
                "price_change_24h": result.price_change_24h,
                "price_change_percentage_24h": result.price_change_percentage_24h,
                "market_cap_usd": result.market_cap_usd,
                "volume_24h_usd": result.volume_24h_usd,
                "last_updated": result.last_updated,
            },
        )

        return result

    async def get_market_history(self, symbol: str, days: int = 7):
        cache_key = f"history:{symbol}:{days}"

        cached = self._cache.get(cache_key)
        if cached:
            return cached["value"]

        data = await self._client.get_market_history(symbol, days)

        prices = [
            {
                "timestamp": int(point[0]),
                "price": point[1],
            }
            for point in data["prices"]
        ]

        self._cache.set(cache_key, prices)

        return prices
