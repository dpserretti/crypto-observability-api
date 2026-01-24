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
