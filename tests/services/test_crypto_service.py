import asyncio
from unittest.mock import AsyncMock

import pytest

from app.clients.coingecko import CoinGeckoClient
from app.core.cache import InMemoryCache
from app.services.crypto_service import CryptoService


@pytest.mark.asyncio
async def test_market_is_fetched_from_client_on_cache_miss():
    client = CoinGeckoClient.__new__(CoinGeckoClient)

    client.get_market_data = AsyncMock(
        return_value={
            "market_data": {
                "current_price": {"usd": 100.0},
                "price_change_24h": 5.0,
                "price_change_percentage_24h": 2.5,
                "market_cap": {"usd": 1_000_000},
                "total_volume": {"usd": 50_000},
            }
        }
    )

    cache = InMemoryCache(ttl_seconds=30)
    service = CryptoService(client, cache)

    result = await service.get_market_summary("bitcoin")

    assert result.price_usd == 100.0
    assert result.cached is False

    client.get_market_data.assert_awaited_once_with("bitcoin")


@pytest.mark.asyncio
async def test_market_is_fetched_from_cache_on_cache_hit():
    client = CoinGeckoClient.__new__(CoinGeckoClient)

    client.get_market_data = AsyncMock(
        return_value={
            "market_data": {
                "current_price": {"usd": 100.0},
                "price_change_24h": 5.0,
                "price_change_percentage_24h": 2.5,
                "market_cap": {"usd": 1_000_000},
                "total_volume": {"usd": 50_000},
            }
        }
    )

    cache = InMemoryCache(ttl_seconds=30)
    service = CryptoService(client, cache)

    first = await service.get_market_summary("bitcoin")
    second = await service.get_market_summary("bitcoin")

    assert first.price_usd == second.price_usd == 100.0
    assert first.cached is False
    assert second.cached is True

    # CoinGecko deve ser chamado apenas uma vez
    client.get_market_data.assert_awaited_once()


@pytest.mark.asyncio
async def test_cache_expires_and_calls_client_again():
    client = CoinGeckoClient.__new__(CoinGeckoClient)

    client.get_market_data = AsyncMock(
        side_effect=[
            {
                "market_data": {
                    "current_price": {"usd": 100.0},
                    "price_change_24h": 5.0,
                    "price_change_percentage_24h": 2.5,
                    "market_cap": {"usd": 1_000_000},
                    "total_volume": {"usd": 50_000},
                }
            },
            {
                "market_data": {
                    "current_price": {"usd": 200.0},
                    "price_change_24h": 10.0,
                    "price_change_percentage_24h": 5.0,
                    "market_cap": {"usd": 2_000_000},
                    "total_volume": {"usd": 80_000},
                }
            },
        ]
    )

    cache = InMemoryCache(ttl_seconds=1)
    service = CryptoService(client, cache)

    first = await service.get_market_summary("bitcoin")
    await asyncio.sleep(1.1)
    second = await service.get_market_summary("bitcoin")

    assert first.price_usd == 100.0
    assert second.price_usd == 200.0
    assert client.get_market_data.await_count == 2
