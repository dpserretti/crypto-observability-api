import asyncio
import logging

import httpx

logger = logging.getLogger("coingecko")


class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client

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
