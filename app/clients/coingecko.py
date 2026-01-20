import httpx


class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=10.0,
        )

    async def get_price(self, coin_id: str, currency: str) -> float:
        response = await self._client.get(
            "/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": currency,
            },
        )
        response.raise_for_status()

        data = response.json()

        try:
            return data[coin_id][currency]
        except KeyError as exc:
            raise ValueError("Invalid response from CoinGecko") from exc

    async def close(self) -> None:
        await self._client.aclose()
