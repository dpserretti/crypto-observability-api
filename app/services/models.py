from datetime import datetime
from typing import NamedTuple


class CryptoPriceResult(NamedTuple):
    price: float
    cached: bool
    last_updated: datetime
