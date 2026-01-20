from app.clients.coingecko import CoinGeckoClient


class CryptoService:
    def __init__(self, client: CoinGeckoClient) -> None:
        self._client = client

    async def get_current_price(self, symbol: str) -> float:
        coin_id = symbol.lower()
        return await self._client.get_price(coin_id, "usd")
