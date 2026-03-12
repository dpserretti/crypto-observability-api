from datetime import datetime

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.services.models import CryptoMarketResult


class CryptoService:
    def __init__(
        self,
        client: CoinGeckoClient,
        cache: InMemoryCache | None,
    ) -> None:
        self._client = client
        self._cache = cache

    async def list_supported_coins(self) -> list[dict]:
        if not self._cache:
            return await self._client.list_coins()

        data, _ = await self._cache.get_or_set_async(
            "coins:list",
            self._client.list_coins,
        )
        return data

    async def get_market_summary(self, symbol: str) -> CryptoMarketResult:
        cache_key = f"market:{symbol.lower()}"

        async def fetch_market_summary_payload() -> dict:
            data = await self._client.get_market_data(symbol.lower())
            market = data["market_data"]
            return {
                "price_usd": market["current_price"]["usd"],
                "price_change_24h": market["price_change_24h"],
                "price_change_percentage_24h": market["price_change_percentage_24h"],
                "market_cap_usd": market["market_cap"]["usd"],
                "volume_24h_usd": market["total_volume"]["usd"],
                "last_updated": datetime.utcnow(),
            }

        if self._cache:
            payload, cached = await self._cache.get_or_set_async(
                cache_key,
                fetch_market_summary_payload,
            )
            return CryptoMarketResult(**payload, cached=cached)

        payload = await fetch_market_summary_payload()
        return CryptoMarketResult(**payload, cached=False)

    async def get_market_history(self, symbol: str, days: int = 7):
        cache_key = f"history:{symbol}:{days}"

        async def fetch_history_points() -> list[dict]:
            data = await self._client.get_market_history(symbol, days)
            return [
                {
                    "timestamp": int(point[0]),
                    "price": point[1],
                }
                for point in data["prices"]
            ]

        if self._cache:
            prices, _ = await self._cache.get_or_set_async(cache_key, fetch_history_points)
            return prices

        return await fetch_history_points()
