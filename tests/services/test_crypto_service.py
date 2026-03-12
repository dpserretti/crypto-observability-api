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


@pytest.mark.asyncio
async def test_coins_are_fetched_from_cache_on_cache_hit():
    client = CoinGeckoClient.__new__(CoinGeckoClient)

    client.list_coins = AsyncMock(
        return_value=[
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
        ]
    )

    cache = InMemoryCache(ttl_seconds=60)
    service = CryptoService(client, cache)

    first = await service.list_supported_coins()
    second = await service.list_supported_coins()

    assert first == second
    client.list_coins.assert_awaited_once()


@pytest.mark.asyncio
async def test_coins_are_fetched_without_cache_when_disabled():
    client = CoinGeckoClient.__new__(CoinGeckoClient)

    client.list_coins = AsyncMock(
        return_value=[
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
        ]
    )

    service = CryptoService(client, cache=None)

    await service.list_supported_coins()
    await service.list_supported_coins()

    assert client.list_coins.await_count == 2


@pytest.mark.asyncio
async def test_concurrent_market_requests_share_single_upstream_call():
    client = CoinGeckoClient.__new__(CoinGeckoClient)

    async def fake_market_data(_symbol: str):
        await asyncio.sleep(0.05)
        return {
            "market_data": {
                "current_price": {"usd": 100.0},
                "price_change_24h": 5.0,
                "price_change_percentage_24h": 2.5,
                "market_cap": {"usd": 1_000_000},
                "total_volume": {"usd": 50_000},
            }
        }

    client.get_market_data = AsyncMock(side_effect=fake_market_data)

    cache = InMemoryCache(ttl_seconds=30)
    service_a = CryptoService(client, cache)
    service_b = CryptoService(client, cache)

    first, second = await asyncio.gather(
        service_a.get_market_summary("bitcoin"),
        service_b.get_market_summary("bitcoin"),
    )

    assert first.price_usd == 100.0
    assert second.price_usd == 100.0
    assert client.get_market_data.await_count == 1
