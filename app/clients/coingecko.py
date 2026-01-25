import asyncio
import logging

import httpx

logger = logging.getLogger("coingecko")


class CoinGeckoClient:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client
        self.BASE_URL = "https://api.coingecko.com/api/v3"

    async def get_price(self, coin_id: str, currency: str) -> float:
        for attempt in range(3):
            try:
                response = await self._client.get(
                    f"{self.BASE_URL}/simple/price",
                    params={
                        "ids": coin_id,
                        "vs_currencies": currency,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data[coin_id][currency]

            except Exception:
                logger.warning(
                    "failed to fetch price",
                    extra={
                        "coin_id": coin_id,
                        "attempt": attempt + 1,
                    },
                )
                if attempt == 2:
                    raise
                await asyncio.sleep(0.3 * (attempt + 1))

    async def list_coins(self) -> list[dict]:
        response = await self._client.get(f"{self.BASE_URL}/coins/list")
        response.raise_for_status()
        return response.json()

    async def get_market_data(self, coin_id: str) -> dict:
        response = await self._client.get(
            f"{self.BASE_URL}/coins/{coin_id}",
            params={
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false",
                "sparkline": "false",
            },
        )
        response.raise_for_status()
        return response.json()
