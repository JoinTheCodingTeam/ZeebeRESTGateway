# pylint: disable=missing-function-docstring
"""Tests for Zeebe gRPC client's publish_message method"""
import time
from typing import Generator
from unittest.mock import Mock, call, AsyncMock

import grpc
import pytest
from httpx import AsyncClient

from zeebe_rest_gateway.app import app, container
from zeebe_rest_gateway.types.message import Message


@pytest.fixture(name='client')
def client_fixture(event_loop) -> Generator[AsyncClient, None, None]:
    client = AsyncClient(app=app, base_url='http://test')
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.mark.asyncio
async def test_publishes_message(client: AsyncClient):
    gateway_stub_mock = AsyncMock()
    with container.gateway_stub.override(gateway_stub_mock):
        response = await client.post('/publish', json={
            'name': 'example_message',
            'correlation_key': '0x3113123123',
            'variables': {
                'value': 5
            },
            'message_id': '234456cx334',
        })
    assert response.status_code == 200
    gateway_stub_mock.PublishMessage.assert_called_once()


@pytest.mark.asyncio
async def test_sends_all_params(client: AsyncClient):
    message = Message(name='example_message', correlation_key='0x3113123123', variables={'value': 5},
                      time_to_live_ms=50, message_id='234456cx334')

    gateway_stub_mock = AsyncMock()
    with container.gateway_stub.override(gateway_stub_mock):
        response = await client.post('/publish', json=message.dict())
    assert response.status_code == 200
    gateway_stub_mock.PublishMessage.assert_called_once_with(message.to_request())


@pytest.mark.asyncio
async def test_requires_params(client: AsyncClient):
    response = await client.post('/publish')
    assert response.status_code == 422
    json = response.json()
    assert json == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.asyncio
async def test_validates_missing_params(client: AsyncClient):
    response = await client.post('/publish', json={})
    assert response.status_code == 422
    json = response.json()
    assert json == {'detail': [{'loc': ['body', 'name'], 'msg': 'field required', 'type': 'value_error.missing'},
                               {'loc': ['body', 'correlation_key'], 'msg': 'field required',
                                'type': 'value_error.missing'},
                               {'loc': ['body', 'variables'], 'msg': 'field required', 'type': 'value_error.missing'},
                               {'loc': ['body', 'message_id'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.asyncio
async def test_validates_param_values(client: AsyncClient):
    response = await client.post('/publish', json={
        'name': '',
        'correlation_key': '',
        'variables': ['!'],
        'time_to_live_ms': 0,
        'message_id': '',
    })
    assert response.status_code == 422
    json = response.json()
    assert json == {'detail': [
        {'ctx': {'limit_value': 1},
         'loc': ['body', 'name'],
         'msg': 'ensure this value has at least 1 characters',
         'type': 'value_error.any_str.min_length'},
        {'ctx': {'limit_value': 1},
         'loc': ['body', 'correlation_key'],
         'msg': 'ensure this value has at least 1 characters',
         'type': 'value_error.any_str.min_length'},
        {'loc': ['body', 'variables'],
         'msg': 'value is not a valid dict',
         'type': 'type_error.dict'},
        {'ctx': {'limit_value': 0},
         'loc': ['body', 'time_to_live_ms'],
         'msg': 'ensure this value is greater than 0',
         'type': 'value_error.number.not_gt'},
        {'ctx': {'limit_value': 1},
         'loc': ['body', 'message_id'],
         'msg': 'ensure this value has at least 1 characters',
         'type': 'value_error.any_str.min_length'}]}


@pytest.mark.asyncio
async def test_retries_zeebe_errors(client: AsyncClient):
    message = Message(name='example_message', correlation_key='0x3113123123', variables={'value': 5},
                      time_to_live_ms=1500, message_id='234456cx334')
    attempts = 7
    delay_ms = 25
    status_codes = [grpc.StatusCode.INTERNAL, grpc.StatusCode.RESOURCE_EXHAUSTED, grpc.StatusCode.UNAVAILABLE]

    settings_mock = Mock()
    settings_mock.zeebe_publish_retry_attempts = attempts
    settings_mock.zeebe_publish_retry_delay_ms = delay_ms

    with container.settings.override(settings_mock):
        for status_code in status_codes:
            gateway_stub_mock = AsyncMock()
            gateway_stub_mock.PublishMessage.side_effect = grpc.aio.AioRpcError(status_code, grpc.aio.Metadata(),
                                                                                grpc.aio.Metadata())
            start_time = time.monotonic()
            with container.gateway_stub.override(gateway_stub_mock):
                response = await client.post('/publish', json=message.dict())
            end_time = time.monotonic()
            assert response.status_code == 500
            gateway_stub_mock.PublishMessage.assert_has_calls([call(message.to_request()) for _ in range(attempts)])
            assert -5 <= (end_time - start_time) - (attempts * delay_ms / 1000) <= 5


@pytest.mark.asyncio
async def test_ignores_message_already_exists(client: AsyncClient):
    message = Message(name='example_message', correlation_key='0x3113123123', variables={'value': 5},
                      time_to_live_ms=50, message_id='234456cx334')
    gateway_stub_mock = AsyncMock()
    gateway_stub_mock.PublishMessage.side_effect = grpc.aio.AioRpcError(grpc.StatusCode.ALREADY_EXISTS,
                                                                        grpc.aio.Metadata(), grpc.aio.Metadata())
    with container.gateway_stub.override(gateway_stub_mock):
        response = await client.post('/publish', json=message.dict())

    assert response.status_code == 200
    gateway_stub_mock.PublishMessage.assert_called_once_with(message.to_request())
