from datetime import datetime

from pydantic import BaseModel


class CryptoCoinResponse(BaseModel):
    id: str
    symbol: str
    name: str


class CryptoMarketResponse(BaseModel):
    price_usd: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_usd: float
    volume_24h_usd: float
    cached: bool
    last_updated: datetime


class CryptoHistoryPoint(BaseModel):
    timestamp: int
    price: float
