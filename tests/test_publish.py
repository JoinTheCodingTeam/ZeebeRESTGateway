import time
from typing import AsyncGenerator
from unittest.mock import Mock, call

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture
from pyzeebe.exceptions import ZeebeBackPressure, ZeebeGatewayUnavailable, ZeebeInternalError, MessageAlreadyExists

from zeebe_rest_gateway.app import zeebe_client, app, ZEEBE_PUBLISH_RETRY_ATTEMPTS


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_publishes_message(client: AsyncClient, mocker: MockerFixture):
    mocker.patch('zeebe_rest_gateway.app.zeebe_client.publish_message')
    resp = await client.post('/publish', json={
        'name': 'example_message',
        'correlation_key': '0x3113123123',
        'variables': {
            'value': 5
        },
        'message_id': '234456cx334',
    })
    assert resp.status_code == 200
    zeebe_client.publish_message.assert_called_once()


@pytest.mark.asyncio
async def test_sends_all_params(client: AsyncClient, mocker: MockerFixture):
    name = 'example_message'
    correlation_key = '0x3113123123'
    variables = {'value': 5}
    time_to_live_in_milliseconds = 50
    message_id = '234456cx334'
    mocker.patch('zeebe_rest_gateway.app.zeebe_client.publish_message')

    resp = await client.post('/publish', json={
        'name': name,
        'correlation_key': correlation_key,
        'variables': variables,
        'time_to_live_in_milliseconds': time_to_live_in_milliseconds,
        'message_id': message_id,
    })
    assert resp.status_code == 200
    zeebe_client.publish_message.assert_called_once_with(name, correlation_key, variables,
                                                         time_to_live_in_milliseconds, message_id)


@pytest.mark.asyncio
async def test_requires_params(client: AsyncClient):
    resp = await client.post('/publish')
    assert resp.status_code == 422
    json = resp.json()
    assert json == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.asyncio
async def test_validates_missing_params(client: AsyncClient):
    resp = await client.post('/publish', json={})
    assert resp.status_code == 422
    json = resp.json()
    assert json == {'detail': [{'loc': ['body', 'name'], 'msg': 'field required', 'type': 'value_error.missing'},
                               {'loc': ['body', 'correlation_key'], 'msg': 'field required',
                                'type': 'value_error.missing'},
                               {'loc': ['body', 'variables'], 'msg': 'field required', 'type': 'value_error.missing'},
                               {'loc': ['body', 'message_id'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.asyncio
async def test_validates_param_values(client: AsyncClient):
    resp = await client.post('/publish', json={
        'name': '',
        'correlation_key': '',
        'variables': ['!'],
        'time_to_live_in_milliseconds': 0,
        'message_id': '',
    })
    assert resp.status_code == 422
    json = resp.json()
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
         'loc': ['body', 'time_to_live_in_milliseconds'],
         'msg': 'ensure this value is greater than 0',
         'type': 'value_error.number.not_gt'},
        {'ctx': {'limit_value': 1},
         'loc': ['body', 'message_id'],
         'msg': 'ensure this value has at least 1 characters',
         'type': 'value_error.any_str.min_length'}]}


@pytest.mark.asyncio
async def test_retries_zeebe_errors(client: AsyncClient, mocker: MockerFixture):
    name = 'example_message'
    correlation_key = '0x3113123123'
    variables = {'value': 5}
    time_to_live_in_milliseconds = 50
    message_id = '234456cx334'
    json = {
        'name': name,
        'correlation_key': correlation_key,
        'variables': variables,
        'time_to_live_in_milliseconds': time_to_live_in_milliseconds,
        'message_id': message_id,
    }
    delay_ms = 0.050
    exceptions = [ZeebeBackPressure, ZeebeGatewayUnavailable, ZeebeInternalError]

    for exception in exceptions:
        mocker.patch('zeebe_rest_gateway.app.ZEEBE_PUBLISH_RETRY_DELAY_MS', delay_ms)

        publish_message_mock = Mock(side_effect=exception())
        mocker.patch('zeebe_rest_gateway.app.zeebe_client.publish_message', publish_message_mock)

        start_time = time.monotonic()
        resp = await client.post('/publish', json=json)
        end_time = time.monotonic()
        assert resp.status_code == 500
        publish_message_mock.assert_has_calls(
            [call(name, correlation_key, variables, time_to_live_in_milliseconds, message_id)
             for _ in range(ZEEBE_PUBLISH_RETRY_ATTEMPTS)])
        assert -5 <= end_time - start_time - delay_ms * ZEEBE_PUBLISH_RETRY_ATTEMPTS <= 5
        mocker.resetall()


@pytest.mark.asyncio
async def test_ignores_message_already_exists(client: AsyncClient, mocker: MockerFixture):
    name = 'example_message'
    correlation_key = '0x3113123123'
    variables = {'value': 5}
    time_to_live_in_milliseconds = 50
    message_id = '234456cx334'
    json = {
        'name': name,
        'correlation_key': correlation_key,
        'variables': variables,
        'time_to_live_in_milliseconds': time_to_live_in_milliseconds,
        'message_id': message_id,
    }

    publish_message_mock = Mock(side_effect=MessageAlreadyExists())
    mocker.patch('zeebe_rest_gateway.app.zeebe_client.publish_message', publish_message_mock)

    resp = await client.post('/publish', json=json)
    assert resp.status_code == 200
    publish_message_mock.assert_called_once_with(name, correlation_key, variables,
                                                 time_to_live_in_milliseconds, message_id)
