from pydantic import BaseModel


class CryptoPriceResponse(BaseModel):
    symbol: str
    price_usd: float
