from datetime import datetime
from typing import NamedTuple


class CryptoPriceResult(NamedTuple):
    price: float
    cached: bool
    last_updated: datetime


class CryptoMarketResult(NamedTuple):
    price_usd: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_usd: float
    volume_24h_usd: float
    cached: bool
    last_updated: datetime
