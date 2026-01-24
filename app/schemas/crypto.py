from datetime import datetime

from pydantic import BaseModel


class CryptoPriceResponse(BaseModel):
    symbol: str
    price_usd: float


class CryptoSummaryResponse(BaseModel):
    symbol: str
    price_usd: float
    cached: bool
    last_updated: datetime


class CryptoMarketResponse(BaseModel):
    symbol: str
    price_usd: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_usd: float
    volume_24h_usd: float
    cached: bool
    last_updated: datetime
