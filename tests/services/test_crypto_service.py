import asyncio
from unittest.mock import AsyncMock

import pytest

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.services.crypto_service import CryptoService


@pytest.mark.asyncio
async def test_price_is_fetched_from_client_on_cache_miss():
    client = CoinGeckoClient.__new__(CoinGeckoClient)
    client.get_price = AsyncMock(return_value=100.0)

    cache = InMemoryCache(ttl_seconds=30)
    service = CryptoService(client, cache)

    price = await service.get_current_price("bitcoin")

    assert price == 100.0
    client.get_price.assert_awaited_once_with("bitcoin", "usd")


@pytest.mark.asyncio
async def test_price_is_fetched_from_cache_on_cache_hit():
    client = CoinGeckoClient.__new__(CoinGeckoClient)
    client.get_price = AsyncMock(return_value=100.0)

    cache = InMemoryCache(ttl_seconds=30)
    service = CryptoService(client, cache)

    first_price = await service.get_current_price("bitcoin")
    second_price = await service.get_current_price("bitcoin")

    assert first_price == second_price == 100.0

    # CoinGecko should be called only once
    client.get_price.assert_awaited_once()


@pytest.mark.asyncio
async def test_cache_expires_and_calls_client_again():
    client = CoinGeckoClient.__new__(CoinGeckoClient)
    client.get_price = AsyncMock(side_effect=[100.0, 200.0])

    cache = InMemoryCache(ttl_seconds=1)
    service = CryptoService(client, cache)

    first_price = await service.get_current_price("bitcoin")
    await asyncio.sleep(1.1)
    second_price = await service.get_current_price("bitcoin")

    assert first_price == 100.0
    assert second_price == 200.0
    assert client.get_price.await_count == 2
