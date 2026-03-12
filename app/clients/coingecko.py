import asyncio
import logging
import random

import httpx

logger = logging.getLogger("coingecko")


class CoinGeckoClient:
    MAX_ATTEMPTS = 3
    MAX_BACKOFF_SECONDS = 8.0

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client
        self.BASE_URL = "https://api.coingecko.com/api/v3"

    async def _request_json(self, endpoint: str, params: dict | None = None):
        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_ATTEMPTS):
            try:
                response = await self._client.get(url, params=params)
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                if not self._should_retry_status(status_code) or attempt == self.MAX_ATTEMPTS - 1:
                    raise

                delay = self._get_retry_delay(
                    attempt=attempt,
                    retry_after=exc.response.headers.get("Retry-After"),
                )

                logger.warning(
                    "coingecko request failed, retrying",
                    extra={
                        "status_code": status_code,
                        "endpoint": endpoint,
                        "attempt": attempt + 1,
                        "delay_seconds": round(delay, 2),
                    },
                )
                await asyncio.sleep(delay)

            except httpx.RequestError:
                if attempt == self.MAX_ATTEMPTS - 1:
                    raise

                delay = self._get_retry_delay(attempt=attempt)
                logger.warning(
                    "coingecko request failed, retrying",
                    extra={
                        "endpoint": endpoint,
                        "attempt": attempt + 1,
                        "delay_seconds": round(delay, 2),
                    },
                )
                await asyncio.sleep(delay)

        raise RuntimeError("coingecko request retries exhausted")

    def _should_retry_status(self, status_code: int) -> bool:
        return status_code == 429 or 500 <= status_code < 600

    def _get_retry_delay(self, attempt: int, retry_after: str | None = None) -> float:
        if retry_after:
            try:
                retry_after_seconds = float(retry_after)
                if retry_after_seconds > 0:
                    return min(retry_after_seconds, self.MAX_BACKOFF_SECONDS)
            except ValueError:
                pass

        base_delay = min(0.5 * (2**attempt), self.MAX_BACKOFF_SECONDS)
        jitter = random.uniform(0.0, 0.25)
        return min(base_delay + jitter, self.MAX_BACKOFF_SECONDS)

    async def get_price(self, coin_id: str, currency: str) -> float:
        data = await self._request_json(
            "/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": currency,
            },
        )
        return data[coin_id][currency]

    async def list_coins(self) -> list[dict]:
        return await self._request_json("/coins/list")

    async def get_market_data(self, coin_id: str) -> dict:
        return await self._request_json(
            f"/coins/{coin_id}",
            params={
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false",
                "sparkline": "false",
                "vs_currency": "usd",
                "ids": coin_id,
                "price_change_percentage": "24h",
            },
        )

    async def get_market_history(
        self,
        coin_id: str,
        days: int = 7,
        vs_currency: str = "usd",
    ):
        return await self._request_json(
            f"/coins/{coin_id}/market_chart",
            params={
                "vs_currency": vs_currency,
                "days": days,
            },
        )
