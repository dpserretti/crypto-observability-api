from unittest.mock import AsyncMock

import httpx
import pytest

import app.clients.coingecko as coingecko_module
from app.clients.coingecko import CoinGeckoClient


def _response(
    status_code: int,
    *,
    json_data: dict | list | None = None,
    headers: dict | None = None,
) -> httpx.Response:
    request = httpx.Request("GET", "https://api.coingecko.com/api/v3/test")
    return httpx.Response(status_code, json=json_data, headers=headers, request=request)


@pytest.mark.asyncio
async def test_market_history_retries_on_429_with_retry_after(monkeypatch):
    http_client = AsyncMock()
    http_client.get = AsyncMock(
        side_effect=[
            _response(429, headers={"Retry-After": "2"}),
            _response(200, json_data={"prices": [[123, 100.0]]}),
        ]
    )

    sleep_mock = AsyncMock()
    monkeypatch.setattr(coingecko_module.asyncio, "sleep", sleep_mock)

    client = CoinGeckoClient(http_client)
    result = await client.get_market_history("bitcoin")

    assert result["prices"] == [[123, 100.0]]
    assert http_client.get.await_count == 2
    sleep_mock.assert_awaited_once_with(2.0)


@pytest.mark.asyncio
async def test_market_data_does_not_retry_on_400(monkeypatch):
    http_client = AsyncMock()
    http_client.get = AsyncMock(
        return_value=_response(400, json_data={"error": "bad request"}),
    )

    sleep_mock = AsyncMock()
    monkeypatch.setattr(coingecko_module.asyncio, "sleep", sleep_mock)

    client = CoinGeckoClient(http_client)

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_market_data("bitcoin")

    assert http_client.get.await_count == 1
    sleep_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_list_coins_retries_on_request_error(monkeypatch):
    request = httpx.Request("GET", "https://api.coingecko.com/api/v3/coins/list")
    http_client = AsyncMock()
    http_client.get = AsyncMock(
        side_effect=[
            httpx.ConnectError("network down", request=request),
            _response(200, json_data=[{"id": "bitcoin"}]),
        ]
    )

    sleep_mock = AsyncMock()
    monkeypatch.setattr(coingecko_module.asyncio, "sleep", sleep_mock)
    monkeypatch.setattr(coingecko_module.random, "uniform", lambda _a, _b: 0.0)

    client = CoinGeckoClient(http_client)
    result = await client.list_coins()

    assert result == [{"id": "bitcoin"}]
    assert http_client.get.await_count == 2
    sleep_mock.assert_awaited_once_with(0.5)
