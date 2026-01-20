import httpx


class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client

    async def get_price(self, coin_id: str, currency: str) -> float:
        response = await self._client.get(
            f"{self.BASE_URL}/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": currency,
            },
        )
        response.raise_for_status()

        data = response.json()

        try:
            return data[coin_id][currency]
        except KeyError as err:
            raise ValueError("Invalid response from CoinGecko") from err
