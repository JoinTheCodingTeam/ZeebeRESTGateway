import time
from unittest.mock import Mock, call

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture
from pyzeebe.exceptions import ZeebeBackPressure, ZeebeGatewayUnavailable, ZeebeInternalError, MessageAlreadyExists

from main import app, zeebe_client, ZEEBE_PUBLISH_RETRY_ATTEMPTS


@pytest.fixture
def client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_publishes_message(client: AsyncClient, mocker: MockerFixture):
    mocker.patch('main.zeebe_client.publish_message')
    resp = await client.post('/publish', json={
        'name': 'example_message',
        'correlation_key': '0x3113123123',
        'variables': {
            'value': 5
        }
    })
    assert resp.status_code == 200
    zeebe_client.publish_message.assert_called_once()


@pytest.mark.asyncio
async def test_sends_all_params(client: AsyncClient, mocker: MockerFixture):
    name = 'example_message'
    correlation_key = '0x3113123123'
    variables = {'value': 5}
    time_to_live_in_milliseconds = 50
    message_id = 'some-uuid'
    mocker.patch('main.zeebe_client.publish_message')

    uuid_mock = Mock()
    uuid_mock.hex = message_id
    mocker.patch('uuid.uuid4', lambda: uuid_mock)

    resp = await client.post('/publish', json={
        'name': name,
        'correlation_key': correlation_key,
        'variables': variables,
        'time_to_live_in_milliseconds': time_to_live_in_milliseconds,
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
                               {'loc': ['body', 'variables'], 'msg': 'field required', 'type': 'value_error.missing'}]}


@pytest.mark.asyncio
async def test_validates_param_values(client: AsyncClient):
    resp = await client.post('/publish', json={
        'name': '',
        'correlation_key': '',
        'variables': ['!'],
        'time_to_live_in_milliseconds': 0,
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
         'type': 'value_error.number.not_gt'}]}


@pytest.mark.asyncio
async def test_retries_zeebe_errors(client: AsyncClient, mocker: MockerFixture):
    name = 'example_message'
    correlation_key = '0x3113123123'
    variables = {'value': 5}
    time_to_live_in_milliseconds = 50
    message_id = 'some-uuid'
    json = {
        'name': name,
        'correlation_key': correlation_key,
        'variables': variables,
        'time_to_live_in_milliseconds': time_to_live_in_milliseconds,
    }
    delay_ms = 0.050
    exceptions = [ZeebeBackPressure, ZeebeGatewayUnavailable, ZeebeInternalError]

    for exception in exceptions:
        uuid_mock = Mock()
        uuid_mock.hex = message_id
        mocker.patch('uuid.uuid4', lambda: uuid_mock)
        mocker.patch('main.ZEEBE_PUBLISH_RETRY_DELAY_MS', delay_ms)

        publish_message_mock = Mock(side_effect=exception())
        mocker.patch('main.zeebe_client.publish_message', publish_message_mock)

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
    message_id = 'some-uuid'
    json = {
        'name': name,
        'correlation_key': correlation_key,
        'variables': variables,
        'time_to_live_in_milliseconds': time_to_live_in_milliseconds,
    }

    uuid_mock = Mock()
    uuid_mock.hex = message_id
    mocker.patch('uuid.uuid4', lambda: uuid_mock)

    publish_message_mock = Mock(side_effect=MessageAlreadyExists())
    mocker.patch('main.zeebe_client.publish_message', publish_message_mock)

    resp = await client.post('/publish', json=json)
    assert resp.status_code == 200
    publish_message_mock.assert_called_once_with(name, correlation_key, variables,
                                                 time_to_live_in_milliseconds, message_id)
